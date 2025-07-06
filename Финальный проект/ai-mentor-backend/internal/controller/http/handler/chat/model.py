from pydantic import BaseModel

from internal import common


class SendMessageToExpert(BaseModel):
    student_id: int
    text: str


class SendMessageToExpertResponse(BaseModel):
    user_message: str
    commands: list[common.Command]

    def to_dict(self):
        return {
            "commands": [command.to_dict() for command in self.commands],
            "user_message": self.user_message,
        }