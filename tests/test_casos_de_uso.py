from datetime import date

import pytest

from financeiro.aplicacao.gerar_relatorio_mensal import GerarRelatorioMensal
from financeiro.aplicacao.registrar_lancamento import RegistrarLancamento
from financeiro.dominio.exportador_relatorio import ExportadorCSV
from financeiro.infraestrutura.repositorio_lancamento_memoria import (
    RepositorioLancamentoMemoria,
)


class TestCasosDeUso:

    def setup_method(self) -> None:
        self.repo = RepositorioLancamentoMemoria()

    def test_caso_de_uso_registrar_lancamento(self) -> None:
        caso_uso = RegistrarLancamento(self.repo)
        lancamento = caso_uso.executar(
            "Feira", 80.0, date(2026, 8, 10), "Alimentação", "debito"
        )
        assert lancamento.id is not None
        assert len(self.repo.listar()) == 1

    def test_caso_de_uso_gerar_relatorio_mensal(self) -> None:
        reg = RegistrarLancamento(self.repo)
        reg.executar("Feira", 80.0, date(2026, 8, 10), "Alimentação", "debito")
        reg.executar("Freela", 1500.0, date(2026, 8, 15), "Renda", "credito")

        caso_relatorio = GerarRelatorioMensal(self.repo, ExportadorCSV())
        relatorio = caso_relatorio.executar(date(2026, 8, 1), date(2026, 8, 31))

        assert "Relatório Financeiro" in relatorio
        assert "Total de débitos: 80.0" in relatorio
        assert "Saldo final: 1420.0" in relatorio