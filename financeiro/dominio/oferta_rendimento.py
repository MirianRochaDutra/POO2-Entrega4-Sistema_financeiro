from datetime import date

from financeiro.dominio.estrategia_rendimento import EstrategiaRendimento


class OfertaRendimento:

    def __init__(
        self,
        codigo: str,
        validade: date,
        estrategia: EstrategiaRendimento,
    ) -> None:
        if not codigo:
            raise ValueError("Código é obrigatório")
        self.codigo = codigo
        self.validade = validade
        self.estrategia = estrategia

    def esta_valida(self, hoje: date) -> bool:
        return hoje <= self.validade

    def calcular_rendimento(self, valor: float, hoje: date) -> float:
        if not self.esta_valida(hoje):
            raise ValueError("Oferta de rendimento expirada")
        return self.estrategia.calcular(valor)