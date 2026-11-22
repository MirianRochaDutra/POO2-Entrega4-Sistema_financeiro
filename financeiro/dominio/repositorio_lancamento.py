from abc import ABC, abstractmethod

from financeiro.dominio.lancamento import Lancamento


class LancamentoNaoEncontradoError(Exception):
    pass


class RepositorioLancamento(ABC):

    @abstractmethod
    def adicionar(self, lancamento: Lancamento) -> None:
        """Guarda um lançamento novo e atribui a ele uma identidade."""
        ...

    @abstractmethod
    def obter(self, id: int) -> Lancamento:
        """Recupera um lançamento por seu ID. Lança LancamentoNaoEncontradoError se não existir."""
        ...

    @abstractmethod
    def listar(self) -> list[Lancamento]:
        """Retorna todos os lançamentos armazenados."""
        ...

    @abstractmethod
    def atualizar(self, lancamento: Lancamento) -> None:
        """Atualiza um lançamento existente."""
        ...