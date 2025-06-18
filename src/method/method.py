from abc import ABC, abstractmethod

class Methode(ABC):
    @abstractmethod
    def solve(self, graph, recuit, court=[]):
        pass