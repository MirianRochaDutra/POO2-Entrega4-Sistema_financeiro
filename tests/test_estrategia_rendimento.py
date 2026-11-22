import pytest

from financeiro.dominio.estrategia_rendimento import (
    RendimentoCDBPreFixado,
    RendimentoPoupanca,
)


class TestEstrategiaRendimento:

    def test_calculo_poupanca(self) -> None:
        est = RendimentoPoupanca(0.5)
        assert est.calcular(1000.0) == 1005.0

    def test_calculo_cdb(self) -> None:
        est = RendimentoCDBPreFixado(10.0)
        assert est.calcular(1000.0) == 1100.0

    def test_percentual_invalido_lanca_erro(self) -> None:
        with pytest.raises(
            ValueError, match="Percentual deve estar entre 0 e 100"
        ):
            RendimentoPoupanca(-1.0)
        with pytest.raises(
            ValueError, match="Percentual deve estar entre 0 e 100"
        ):
            RendimentoCDBPreFixado(105.0)