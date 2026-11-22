from datetime import date

import pytest

from financeiro.composicao import montar_aplicacao


class TestComposicao:

    @pytest.mark.parametrize("armazenamento", ["memoria", "sqlite"])
    def test_aplicacao_executa_fluxo_nas_duas_configuracoes(
        self, armazenamento: str
    ) -> None:
        app = montar_aplicacao(armazenamento=armazenamento)

        lancamento = app.registrar_lancamento.executar(
            "Restaurante", 120.0, date(2026, 8, 12), "Alimentação", "debito"
        )
        assert lancamento.id is not None

        relatorio = app.gerar_relatorio_mensal.executar(
            date(2026, 8, 1), date(2026, 8, 31)
        )
        assert "Total de débitos: 120.0" in relatorio