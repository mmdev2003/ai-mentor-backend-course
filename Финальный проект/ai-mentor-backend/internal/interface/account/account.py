from abc import abstractmethod
from typing import Protocol

from internal import model


class IAccountRepo(Protocol):
    @abstractmethod
    async def create_account(self, login: str, password: str) -> int: pass

    @abstractmethod
    async def get_account_by_login(self, login: str) -> list[model.Account]: pass
