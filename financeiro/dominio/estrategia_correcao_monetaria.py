from abc import ABC, abstractmethod


class EstrategiaCorrecaoMonetaria(ABC):

    @abstractmethod
    def calcular(self, valor: float) -> float:
        ...


class CorrecaoIPCA(EstrategiaCorrecaoMonetaria):

    def __init__(self, percentual: float) -> None:
        if not (0 <= percentual <= 100):
            raise ValueError("Percentual deve estar entre 0 e 100")
        self.percentual = percentual

    def calcular(self, valor: float) -> float:
        return round(valor * (1 + self.percentual / 100), 2)


class CorrecaoINPC(EstrategiaCorrecaoMonetaria):

    def __init__(self, percentual: float) -> None:
        if not (0 <= percentual <= 100):
            raise ValueError("Percentual deve estar entre 0 e 100")
        self.percentual = percentual

    def calcular(self, valor: float) -> float:
        return round(valor * (1 + self.percentual / 100), 2)