from datetime import date

from financeiro.dominio.categoria import Categoria


class Lancamento:

    def __init__(
        self,
        descricao: str,
        valor: float,
        data: date,
        categoria: Categoria,
        tipo: str,
    ) -> None:
        if not descricao:
            raise ValueError("Descrição é obrigatória")
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
        if tipo not in ("debito", "credito"):
            raise ValueError("Tipo deve ser 'debito' ou 'credito'")

        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria = categoria
        self.tipo = tipo
        self._id: int | None = None

    @property
    def id(self) -> int | None:
        return self._id

    def atribuir_id(self, id: int) -> None:
        if self._id is not None:
            raise ValueError("Lançamento já possui identidade")
        self._id = id

    def eh_debito(self) -> bool:
        return self.tipo == "debito"

    def eh_credito(self) -> bool:
        return self.tipo == "credito"

    @classmethod
    def reconstituir(
        cls,
        id: int,
        descricao: str,
        valor: float,
        data: date,
        categoria: Categoria,
        tipo: str,
    ) -> "Lancamento":
        lancamento = cls(descricao, valor, data, categoria, tipo)
        lancamento._id = id
        return lancamento