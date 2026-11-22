import pytest

from financeiro.dominio.estrategia_juros import JurosCompostos, JurosSimples


class TestEstrategiaJuros:

    def test_juros_simples(self) -> None:
        est = JurosSimples()
        assert est.calcular(1000.0, 0.1, 2) == 1200.0

    def test_juros_compostos(self) -> None:
        est = JurosCompostos()
        assert est.calcular(1000.0, 0.1, 2) == 1210.0

    def test_valores_negativos_lancam_erro(self) -> None:
        est = JurosSimples()
        with pytest.raises(ValueError):
            est.calcular(-100.0, 0.1, 2)
        with pytest.raises(ValueError):
            est.calcular(100.0, -0.1, 2)
        with pytest.raises(ValueError):
            est.calcular(100.0, 0.1, -1)