from financeiro.dominio.lancamento import Lancamento
from financeiro.dominio.repositorio_lancamento import (
    LancamentoNaoEncontradoError,
    RepositorioLancamento,
)


class RepositorioLancamentoMemoria(RepositorioLancamento):

    def __init__(self) -> None:
        self._lancamentos: dict[int, Lancamento] = {}
        self._proximo_id = 1

    def adicionar(self, lancamento: Lancamento) -> None:
        lancamento.atribuir_id(self._proximo_id)
        self._lancamentos[self._proximo_id] = lancamento
        self._proximo_id += 1

    def obter(self, id: int) -> Lancamento:
        if id not in self._lancamentos:
            raise LancamentoNaoEncontradoError(
                f"Lançamento {id} não encontrado"
            )
        return self._lancamentos[id]

    def listar(self) -> list[Lancamento]:
        return list(self._lancamentos.values())

    def atualizar(self, lancamento: Lancamento) -> None:
        if lancamento.id is None or lancamento.id not in self._lancamentos:
            raise LancamentoNaoEncontradoError("Lançamento nunca foi adicionado")
        self._lancamentos[lancamento.id] = lancamento