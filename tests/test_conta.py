import pytest

from financeiro.dominio.conta import Conta


class TestConta:

    def test_criar_conta_com_saldo_inicial(self) -> None:
        conta = Conta("Corrente", 100.0)
        assert conta.nome == "Corrente"
        assert conta.saldo == 100.0

    def test_debitar_valor_positivo(self) -> None:
        conta = Conta("Corrente", 100.0)
        conta.debitar(40.0)
        assert conta.saldo == 60.0

    def test_creditar_valor_positivo(self) -> None:
        conta = Conta("Corrente", 100.0)
        conta.creditar(50.0)
        assert conta.saldo == 150.0

    def test_debitar_valor_invalido_gera_erro(self) -> None:
        conta = Conta("Corrente", 100.0)
        with pytest.raises(ValueError):
            conta.debitar(-10.0)

    def test_creditar_valor_invalido_gera_erro(self) -> None:
        conta = Conta("Corrente", 100.0)
        with pytest.raises(ValueError):
            conta.creditar(0.0)