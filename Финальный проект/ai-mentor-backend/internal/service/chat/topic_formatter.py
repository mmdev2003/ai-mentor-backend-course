import json

from internal import model


class EducationDataFormatter:
    def __init__(self, topics: list[model.Topic], blocks: list[model.Block], chapters: list[model.Chapter]):
        self.topics = topics
        self.blocks = blocks
        self.chapters = chapters

    def to_flat_json(self) -> str:
        """Плоская структура JSON - все сущности в отдельных массивах"""
        data = {
            "topics": [topic.to_dict() for topic in self.topics],
            "blocks": [block.to_dict() for block in self.blocks],
            "chapters": [chapter.to_dict() for chapter in self.chapters]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def to_hierarchical_json(self) -> str:
        """Иерархическая структура JSON - topics содержат blocks, blocks содержат chapters"""
        # Группируем блоки по topic_id
        blocks_by_topic = {}
        for block in self.blocks:
            if block.topic_id not in blocks_by_topic:
                blocks_by_topic[block.topic_id] = []
            blocks_by_topic[block.topic_id].append(block)

        # Группируем главы по block_id
        chapters_by_block = {}
        for chapter in self.chapters:
            if chapter.block_id not in chapters_by_block:
                chapters_by_block[chapter.block_id] = []
            chapters_by_block[chapter.block_id].append(chapter)

        # Строим иерархическую структуру
        topics_data = []
        for topic in self.topics:
            topic_dict = topic.to_dict()
            topic_dict["blocks"] = []

            # Добавляем блоки для текущей темы
            if topic.id in blocks_by_topic:
                for block in blocks_by_topic[topic.id]:
                    block_dict = block.to_dict()
                    block_dict["chapters"] = []

                    # Добавляем главы для текущего блока
                    if block.id in chapters_by_block:
                        for chapter in chapters_by_block[block.id]:
                            block_dict["chapters"].append(chapter.to_dict())

                    topic_dict["blocks"].append(block_dict)

            topics_data.append(topic_dict)

        return json.dumps({"topics": topics_data}, ensure_ascii=False, indent=2)