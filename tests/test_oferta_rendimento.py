from datetime import date

import pytest

from financeiro.dominio.estrategia_rendimento import RendimentoPoupanca
from financeiro.dominio.oferta_rendimento import OfertaRendimento


class TestOfertaRendimento:

    def setup_method(self) -> None:
        self.est = RendimentoPoupanca(1.0)
        self.oferta = OfertaRendimento("OF001", date(2026, 12, 31), self.est)

    def test_oferta_valida(self) -> None:
        hoje = date(2026, 8, 10)
        assert self.oferta.esta_valida(hoje) is True
        assert self.oferta.calcular_rendimento(1000.0, hoje) == 1010.0

    def test_oferta_expirada_lanca_erro(self) -> None:
        hoje = date(2027, 1, 1)
        assert self.oferta.esta_valida(hoje) is False
        with pytest.raises(ValueError, match="Oferta de rendimento expirada"):
            self.oferta.calcular_rendimento(1000.0, hoje)