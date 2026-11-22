import sqlite3

import pytest

from financeiro.infraestrutura.esquema_sqlite import criar_esquema
from financeiro.infraestrutura.repositorio_lancamento_memoria import (
    RepositorioLancamentoMemoria,
)
from financeiro.infraestrutura.repositorio_lancamento_sqlite import (
    RepositorioLancamentoSQLite,
)


@pytest.fixture(params=["memoria", "sqlite"])
def repositorio_lancamento(request):
    """Fixture parametrizada que executa a mesma suíte de testes de contrato para Memória e SQLite."""
    if request.param == "memoria":
        yield RepositorioLancamentoMemoria()
    else:
        conexao = sqlite3.connect(":memory:")
        criar_esquema(conexao)
        yield RepositorioLancamentoSQLite(conexao)
        conexao.close()