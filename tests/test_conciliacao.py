from datetime import date

import pytest

from financeiro.dominio.categoria import Categoria
from financeiro.dominio.conciliacao import Conciliacao
from financeiro.dominio.lancamento import Lancamento


class TestConciliacao:

    def setup_method(self) -> None:
        cat = Categoria("Geral")
        self.l1 = Lancamento(
            "Compra 1", 100.0, date(2026, 8, 10), cat, "debito"
        )
        self.l2 = Lancamento(
            "Pagamento", 100.0, date(2026, 8, 10), cat, "credito"
        )
        self.l3 = Lancamento(
            "Compra 2", 50.0, date(2026, 8, 11), cat, "debito"
        )

    def test_conciliacao_bate(self) -> None:
        c = Conciliacao([self.l1], [self.l2])
        assert c.esta_conciliada() is True
        c.conciliar()

    def test_conciliacao_nao_bate_gera_erro(self) -> None:
        c = Conciliacao([self.l1, self.l3], [self.l2])
        assert c.esta_conciliada() is False
        with pytest.raises(ValueError, match="Conciliação não bate"):
            c.conciliar()