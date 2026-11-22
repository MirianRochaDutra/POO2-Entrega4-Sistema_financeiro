import pytest

from financeiro.dominio.categoria import Categoria


class TestCategoria:

    def test_criar_categoria_com_sucesso(self) -> None:
        cat = Categoria("Alimentação")
        assert cat.nome == "Alimentação"

    def test_categoria_sem_nome_gera_erro(self) -> None:
        with pytest.raises(ValueError, match="Nome da categoria é obrigatório"):
            Categoria("")