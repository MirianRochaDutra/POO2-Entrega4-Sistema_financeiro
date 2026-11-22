from datetime import date

import pytest

from financeiro.dominio.categoria import Categoria
from financeiro.dominio.fechamento import Fechamento
from financeiro.dominio.lancamento import Lancamento


class TestFechamento:

    def setup_method(self) -> None:
        cat = Categoria("Geral")
        self.debito = Lancamento(
            "Mercado", 200.0, date(2026, 8, 10), cat, "debito"
        )
        self.credito = Lancamento(
            "Salário", 3000.0, date(2026, 8, 5), cat, "credito"
        )

    def test_calculo_totais_e_saldo(self) -> None:
        f = Fechamento(
            date(2026, 8, 1), date(2026, 8, 31), [self.debito, self.credito]
        )
        assert f.quantidade_lancamentos() == 2
        assert f.total_debitos() == 200.0
        assert f.total_creditos() == 3000.0
        assert f.saldo() == 2800.0

    def test_lancamento_fora_do_periodo_gera_erro(self) -> None:
        cat = Categoria("Geral")
        fora = Lancamento("Antigo", 100.0, date(2026, 7, 31), cat, "debito")
        with pytest.raises(
            ValueError, match="Existe lançamento fora do período"
        ):
            Fechamento(date(2026, 8, 1), date(2026, 8, 31), [fora])