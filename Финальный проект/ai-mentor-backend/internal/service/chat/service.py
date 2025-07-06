import json
from opentelemetry.trace import StatusCode, SpanKind

from internal import interface, common


class ChatService(interface.IChatService):

    def __init__(
            self,
            tel: interface.ITelemetry,
            llm_client: interface.ILLMClient,
            prompt_generator: interface.IPromptGenerator,
            student_repo: interface.IStudentRepo,
            topic_repo: interface.ITopicRepo,
            chat_repo: interface.IChatRepo,
            account_repo: interface.IAccountRepo,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.llm_client = llm_client
        self.prompt_generator = prompt_generator
        self.student_repo = student_repo
        self.topic_repo = topic_repo
        self.chat_repo = chat_repo
        self.account_repo = account_repo

    async def send_message_to_expert(self, student_id: int, text: str) -> tuple[str, list[common.Command]]:
        """Обработка сообщений для эксперта по регистрации"""
        with self.tracer.start_as_current_span(
                "ChatService.send_message_to_expert",
                kind=SpanKind.INTERNAL,
                attributes={"student_id": student_id, "text": text}
        ) as span:
            try:
                student = (await self.student_repo.get_by_id(student_id))[0]

                chat = await self.chat_repo.get_chat_by_student_id(student_id)
                if not chat:
                    _ = await self.chat_repo.create_chat(student_id)
                    chat = await self.chat_repo.get_chat_by_student_id(student_id)
                chat_id = chat[0].id

                _ = await self.chat_repo.create_message(chat_id, common.Roles.user, text)

                if student.current_expert == common.Experts.registrator:
                    system_prompt = await self.prompt_generator.get_registrator_prompt()

                if student.current_expert == common.Experts.interview:
                    system_prompt = await self.prompt_generator.get_interview_expert_prompt(student_id)

                if student.current_expert == common.Experts.teacher:
                    system_prompt = await self.prompt_generator.get_teacher_prompt(student_id)

                if student.current_expert == common.Experts.test:
                    system_prompt = await self.prompt_generator.get_test_expert_prompt(student_id)

                chat_history = await self.chat_repo.get_messages(chat_id)

                # Получаем ответ от LLM
                llm_response = await self.llm_client.generate(
                    history=chat_history,
                    system_prompt=system_prompt,
                    temperature=0.3
                )
                response_data = await self._parse_llm_response(llm_response)

                user_message = response_data["user_message"]
                commands = [common.Command(**command) for command in
                            response_data.get("metadata", {}).get("commands", [])]

                _ = await self.chat_repo.create_message(chat_id, common.Roles.assistant, user_message)

                if student.current_expert == common.Experts.registrator:
                    await self._execute_registrator_commands(student_id, commands)

                if student.current_expert == common.Experts.interview:
                    await self._execute_interview_commands(student_id, commands)

                if student.current_expert == common.Experts.teacher:
                    await self._execute_teacher_commands(student_id, commands)

                if student.current_expert == common.Experts.test:
                    await self._execute_test_commands(student_id, commands)

                span.set_status(StatusCode.OK)
                return user_message, commands

            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def _parse_llm_response(self, response: str) -> dict:
        try:
            # Убираем возможные лишние символы вокруг JSON
            response = response.strip()

            # Удаляем markdown форматирование
            if response.startswith("```json"):
                response = response[7:]
            elif response.startswith("```"):
                response = response[3:]

            if response.endswith("```"):
                response = response[:-3]

            response = response.strip()

            # Парсим JSON
            parsed = json.loads(response)

            # Проверяем обязательные поля
            if "user_message" not in parsed:
                self.logger.warning("Отсутствует поле 'user_message' в ответе LLM")
                return {
                    "user_message": "Извините, произошла ошибка обработки ответа. Попробуйте еще раз.",
                    "metadata": {"commands": []}
                }

            # Проверяем структуру metadata
            if "metadata" not in parsed:
                parsed["metadata"] = {"commands": []}
            elif "commands" not in parsed["metadata"]:
                parsed["metadata"]["commands"] = []

            return parsed

        except json.JSONDecodeError as e:
            self.logger.error(f"Ошибка парсинга JSON от LLM: {e}, response: {response}")
            return {
                "user_message": "Извините, произошла ошибка обработки ответа. Попробуйте переформулировать вопрос.",
                "metadata": {"commands": []}
            }
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка при обработке ответа LLM: {e}")
            return {
                "user_message": "Произошла системная ошибка. Обратитесь к администратору.",
                "metadata": {"commands": []}
            }

    async def _execute_registrator_commands(self, student_id: int, commands: list[common.Command]):
        for command in commands:
            command_name = command.name
            params = command.params

            if command_name == "register_student":
                await self._register_student(**params)
            elif command_name == "login_student":
                await self._login_student(**params)
            elif command_name == "switch_to_next_expert":
                await self._switch_expert(student_id, params.get("next_expert"))

    async def _execute_interview_commands(self, student_id: int, commands: list[common.Command]):
        for command in commands:
            command_name = command.name
            params = command.params

            if command_name == "update_student_background":
                background = params
                await self._update_student_background(student_id, background)
            elif command_name == "switch_to_next_expert":
                next_expert = params["next_expert"]
                await self._switch_expert(student_id, next_expert)

    async def _execute_teacher_commands(self, student_id: int, commands: list[common.Command]):
        for command in commands:
            command_name = command.name
            params = command.params

            if command_name == "change_edu_content":
                topic_id = params["topic_id"]
                topic_name = params["topic_name"]
                block_id = params["block_id"]
                block_name = params["block_name"]
                chapter_id = params["chapter_id"]
                chapter_name = params["chapter_name"]
                await self._change_edu_content(
                    student_id,
                    topic_id,
                    topic_name,
                    block_id,
                    block_name,
                    chapter_id,
                    chapter_name,
                )
            elif command_name == "switch_to_next_expert":
                next_expert = params["next_expert"]
                await self._switch_expert(student_id, next_expert)

    async def _execute_test_commands(self, student_id: int, commands: list[common.Command]):
        for command in commands:
            command_name = command.name
            params = command.params

            if command_name == "approve_topic":
                topic_id = params["topic_id"]
                topic_name = params["topic_name"]
                await self._approve_topic(student_id, topic_id, topic_name)

            elif command_name == "approve_block":
                block_id = params["block_id"]
                block_name = params["block_name"]
                await self._approve_block(student_id, block_id, block_name)

            elif command_name == "approve_chapter":
                chapter_id = params["chapter_id"]
                chapter_name = params["chapter_name"]
                await self._approve_chapter(student_id, chapter_id, chapter_name)

            elif command_name == "switch_to_next_expert":
                await self._switch_expert(student_id, params.get("next_expert"))

    # Методы для работы с данными
    async def _register_student(self, login: str, password: str) -> tuple[int, int]:
        account_id = await self.account_repo.create_account(login, password)
        student_id = await self.student_repo.create_student(account_id)
        return account_id, student_id

    async def _login_student(self, login: str, password: str):
        account = await self.account_repo.get_account_by_login(login)
        if not account:
            raise ValueError("Аккаунт не найден")

        if account[0].password != password:
            raise ValueError("Неверный пароль")

        return account[0].id

    async def _update_student_background(self, student_id: int, background: dict):
        await self.student_repo.update_student_background(student_id, background)

    async def _change_edu_content(
            self,
            student_id: int,
            topic_id: int,
            topic_name: str,
            block_id: int,
            block_name: str,
            chapter_id: int,
            chapter_name: str
    ):
        await self.topic_repo.update_current_topic(student_id, topic_id, topic_name)
        await self.topic_repo.update_current_block(student_id, block_id, block_name)
        await self.topic_repo.update_current_chapter(student_id, chapter_id, chapter_name)

    async def _approve_topic(self, student_id: int, topic_id: int, topic_name: str):
        await self.student_repo.add_topic_to_approved_topics(student_id, topic_id, topic_name)

    async def _approve_block(self, student_id: int, block_id: int, block_name: str):
        await self.student_repo.add_block_to_approved_blocks(student_id, block_id, block_name)

    async def _approve_chapter(self, student_id: int, chapter_id: int, chapter_name: str):
        await self.student_repo.add_chapter_to_approved_chapters(student_id, chapter_id, chapter_name)

    async def _switch_expert(self, student_id: int, next_expert: str):
        await self.student_repo.change_current_expert(student_id, next_expert)
