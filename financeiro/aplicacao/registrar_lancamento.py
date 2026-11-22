from datetime import date

from financeiro.dominio.categoria import Categoria
from financeiro.dominio.lancamento import Lancamento
from financeiro.dominio.repositorio_lancamento import RepositorioLancamento


class RegistrarLancamento:
    """Caso de uso: criar e persistir um único lançamento financeiro."""

    def __init__(self, repositorio_lancamento: RepositorioLancamento) -> None:
        self._repositorio = repositorio_lancamento

    def executar(
        self,
        descricao: str,
        valor: float,
        data: date,
        categoria_nome: str,
        tipo: str,
    ) -> Lancamento:
        categoria = Categoria(categoria_nome)
        lancamento = Lancamento(descricao, valor, data, categoria, tipo)
        self._repositorio.adicionar(lancamento)
        return lancamento