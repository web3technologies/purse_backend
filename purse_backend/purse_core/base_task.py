from abc import ABC, abstractmethod
from collections import defaultdict


class BaseTask(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.results = defaultdict(list)

    @abstractmethod
    def run(self, *args, **kwargs):
        return self.results