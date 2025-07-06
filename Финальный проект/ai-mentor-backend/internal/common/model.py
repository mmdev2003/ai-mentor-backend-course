from dataclasses import dataclass


@dataclass
class Command:
    description: str
    name: str
    params: dict

    def to_dict(self):
        return {
            "name": self.name,
            "params": self.params,
            "description": self.description
        }
