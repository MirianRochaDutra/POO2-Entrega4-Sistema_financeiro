from datetime import date

import pytest

from financeiro.dominio.categoria import Categoria
from financeiro.dominio.extrato import Extrato
from financeiro.dominio.fechamento import Fechamento
from financeiro.dominio.lancamento import Lancamento


class TestExtrato:

    def test_consolidação_multiplos_fechamentos(self) -> None:
        cat = Categoria("Geral")
        l1 = Lancamento("Debito 1", 100.0, date(2026, 8, 5), cat, "debito")
        l2 = Lancamento("Credito 1", 500.0, date(2026, 8, 20), cat, "credito")

        f1 = Fechamento(date(2026, 8, 1), date(2026, 8, 15), [l1])
        f2 = Fechamento(date(2026, 8, 16), date(2026, 8, 31), [l2])

        extrato = Extrato(date(2026, 8, 1), date(2026, 8, 31), [f1, f2])
        assert extrato.quantidade_lancamentos() == 2
        assert extrato.total_debitos() == 100.0
        assert extrato.total_creditos() == 500.0
        assert extrato.saldo_final() == 400.0