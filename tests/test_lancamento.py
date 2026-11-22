from datetime import date

import pytest

from financeiro.dominio.categoria import Categoria
from financeiro.dominio.lancamento import Lancamento


class TestLancamento:

    def setup_method(self) -> None:
        self.cat = Categoria("Alimentação")

    def test_criar_lancamento_debito(self) -> None:
        l = Lancamento("Mercado", 150.0, date(2026, 8, 10), self.cat, "debito")
        assert l.descricao == "Mercado"
        assert l.valor == 150.0
        assert l.eh_debito() is True
        assert l.eh_credito() is False
        assert l.id is None

    def test_atribuir_id_com_sucesso(self) -> None:
        l = Lancamento("Mercado", 150.0, date(2026, 8, 10), self.cat, "debito")
        l.atribuir_id(1)
        assert l.id == 1

    def test_atribuir_id_duplicado_gera_erro(self) -> None:
        l = Lancamento("Mercado", 150.0, date(2026, 8, 10), self.cat, "debito")
        l.atribuir_id(1)
        with pytest.raises(ValueError, match="Lançamento já possui identidade"):
            l.atribuir_id(2)

    def test_tipo_invalido_gera_erro(self) -> None:
        with pytest.raises(
            ValueError, match="Tipo deve ser 'debito' ou 'credito'"
        ):
            Lancamento("Teste", 100.0, date(2026, 8, 10), self.cat, "outro")