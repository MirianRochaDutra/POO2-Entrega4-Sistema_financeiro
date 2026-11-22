import pytest

from financeiro.dominio.estrategia_correcao_monetaria import (
    CorrecaoINPC,
    CorrecaoIPCA,
)


class TestEstrategiaCorrecaoMonetaria:

    def test_correcao_ipca(self) -> None:
        est = CorrecaoIPCA(4.5)
        assert est.calcular(100.0) == 104.5

    def test_correcao_inpc(self) -> None:
        est = CorrecaoINPC(5.0)
        assert est.calcular(100.0) == 105.0

    def test_percentual_invalido_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            CorrecaoIPCA(-0.1)
        with pytest.raises(ValueError):
            CorrecaoINPC(101.0)