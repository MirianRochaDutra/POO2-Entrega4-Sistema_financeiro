from datetime import date

from financeiro.dominio.exportador_relatorio import ExportadorRelatorio
from financeiro.dominio.extrato import Extrato
from financeiro.dominio.fechamento import Fechamento
from financeiro.dominio.repositorio_lancamento import RepositorioLancamento


class GerarRelatorioMensal:
    """Caso de uso: consultar lançamentos do repositório, consolidar Extrato e gerar relatório formatado."""

    def __init__(
        self,
        repositorio_lancamento: RepositorioLancamento,
        exportador: ExportadorRelatorio,
    ) -> None:
        self._repositorio = repositorio_lancamento
        self._exportador = exportador

    def executar(self, inicio: date, fim: date) -> str:
        todos_lancamentos = self._repositorio.listar()
        lancamentos_periodo = [
            l for l in todos_lancamentos if inicio <= l.data <= fim
        ]

        fechamento = Fechamento(inicio, fim, lancamentos_periodo)
        extrato = Extrato(inicio, fim, [fechamento])

        return self._exportador.exportar(extrato)