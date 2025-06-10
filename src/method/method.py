from abc import ABC, abstractmethod

class Methode(ABC):
    @abstractmethod
    def resoudre(self, graph, court=[]):
        pass