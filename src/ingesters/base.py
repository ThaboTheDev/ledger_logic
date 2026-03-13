from abc import ABC, abstractmethod
from typing import List
from models.transaction import Transaction

class Base(ABC):
    @abstractmethod
    def parse(file_path: str) -> List[Transaction]:
        pass