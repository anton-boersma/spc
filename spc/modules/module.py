from abc import ABC, abstractmethod


class Module(ABC):
    @abstractmethod
    def update(self):
        raise NotImplementedError("update methode not implemented")
