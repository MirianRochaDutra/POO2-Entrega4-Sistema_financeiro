from abc import ABC, abstractmethod


class EstrategiaJuros(ABC):

    @abstractmethod
    def calcular(self, capital: float, taxa: float, tempo: int) -> float:
        ...


class JurosSimples(EstrategiaJuros):

    def calcular(self, capital: float, taxa: float, tempo: int) -> float:
        if capital < 0 or taxa < 0 or tempo < 0:
            raise ValueError("Capital, taxa e tempo devem ser não negativos")
        return round(capital + (capital * taxa * tempo), 2)


class JurosCompostos(EstrategiaJuros):

    def calcular(self, capital: float, taxa: float, tempo: int) -> float:
        if capital < 0 or taxa < 0 or tempo < 0:
            raise ValueError("Capital, taxa e tempo devem ser não negativos")
        return round(capital * ((1 + taxa) ** tempo), 2)