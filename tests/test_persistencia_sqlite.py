import sqlite3
from datetime import date

from financeiro.dominio.categoria import Categoria
from financeiro.dominio.lancamento import Lancamento
from financeiro.infraestrutura.esquema_sqlite import criar_esquema
from financeiro.infraestrutura.repositorio_lancamento_sqlite import (
    RepositorioLancamentoSQLite,
)


class TestPersistenciaSQLite:

    def test_dados_sobrevivem_ao_reinicio(self, tmp_path) -> None:
        caminho_db = str(tmp_path / "financeiro.db")

        # 1. Abre conexão, grava um lançamento e fecha
        conexao1 = sqlite3.connect(caminho_db)
        criar_esquema(conexao1)
        repo1 = RepositorioLancamentoSQLite(conexao1)

        cat = Categoria("Geral")
        lancamento = Lancamento(
            "Aluguel", 1200.0, date(2026, 8, 1), cat, "debito"
        )
        repo1.adicionar(lancamento)
        id_salvo = lancamento.id
        conexao1.close()

        # 2. "Reinicia" abrindo nova conexão no mesmo arquivo
        conexao2 = sqlite3.connect(caminho_db)
        repo2 = RepositorioLancamentoSQLite(conexao2)
        relido = repo2.obter(id_salvo)

        assert relido.descricao == "Aluguel"
        assert relido.valor == 1200.0
        conexao2.close()