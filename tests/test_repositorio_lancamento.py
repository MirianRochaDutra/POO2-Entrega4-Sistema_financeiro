from datetime import date

import pytest

from financeiro.dominio.categoria import Categoria
from financeiro.dominio.lancamento import Lancamento
from financeiro.dominio.repositorio_lancamento import (
    LancamentoNaoEncontradoError,
)


class TestRepositorioLancamentoContrato:

    def setup_method(self) -> None:
        self.categoria = Categoria("Alimentação")
        self.lancamento = Lancamento(
            "Mercado", 250.0, date(2026, 8, 10), self.categoria, "debito"
        )

    def test_adicionar_atribui_identidade(
        self, repositorio_lancamento
    ) -> None:
        repositorio_lancamento.adicionar(self.lancamento)
        assert self.lancamento.id is not None

    def test_obter_lancamento_por_id(self, repositorio_lancamento) -> None:
        repositorio_lancamento.adicionar(self.lancamento)
        obtido = repositorio_lancamento.obter(self.lancamento.id)
        assert obtido.id == self.lancamento.id
        assert obtido.descricao == "Mercado"
        assert obtido.valor == 250.0

    def test_obter_inexistente_gera_erro(
        self, repositorio_lancamento
    ) -> None:
        with pytest.raises(LancamentoNaoEncontradoError):
            repositorio_lancamento.obter(999)

    def test_listar_lancamentos(self, repositorio_lancamento) -> None:
        repositorio_lancamento.adicionar(self.lancamento)
        outros = Lancamento(
            "Salário", 5000.0, date(2026, 8, 5), self.categoria, "credito"
        )
        repositorio_lancamento.adicionar(outros)
        lista = repositorio_lancamento.listar()
        assert len(lista) == 2

    def test_atualizar_lancamento(self, repositorio_lancamento) -> None:
        repositorio_lancamento.adicionar(self.lancamento)
        self.lancamento.valor = 300.0
        repositorio_lancamento.atualizar(self.lancamento)
        atualizado = repositorio_lancamento.obter(self.lancamento.id)
        assert atualizado.valor == 300.0