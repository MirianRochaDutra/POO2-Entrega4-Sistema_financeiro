import sqlite3
from datetime import date
from financeiro.dominio.categoria import Categoria
from financeiro.dominio.lancamento import Lancamento
from financeiro.dominio.repositorio_lancamento import (
    LancamentoNaoEncontradoError,
    RepositorioLancamento,
)


class RepositorioLancamentoSQLite(RepositorioLancamento):

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

    def adicionar(self, lancamento: Lancamento) -> None:
        with self._conexao:
            cursor = self._conexao.execute(
                "INSERT INTO lancamento (descricao, valor, data, categoria, tipo) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    lancamento.descricao,
                    lancamento.valor,
                    lancamento.data.isoformat(),
                    lancamento.categoria.nome,
                    lancamento.tipo,
                ),
            )
            lancamento.atribuir_id(cursor.lastrowid)

    def obter(self, id: int) -> Lancamento:
        linha = self._conexao.execute(
            "SELECT id, descricao, valor, data, categoria, tipo FROM lancamento WHERE id = ?",
            (id,),
        ).fetchone()
        if linha is None:
            raise LancamentoNaoEncontradoError(
                f"Lançamento {id} não encontrado"
            )
        return self._reconstituir(linha)

    def listar(self) -> list[Lancamento]:
        linhas = self._conexao.execute(
            "SELECT id, descricao, valor, data, categoria, tipo FROM lancamento ORDER BY id"
        ).fetchall()
        return [self._reconstituir(linha) for linha in linhas]

    def atualizar(self, lancamento: Lancamento) -> None:
        with self._conexao:
            cursor = self._conexao.execute(
                "UPDATE lancamento SET descricao = ?, valor = ?, data = ?, categoria = ?, tipo = ? "
                "WHERE id = ?",
                (
                    lancamento.descricao,
                    lancamento.valor,
                    lancamento.data.isoformat(),
                    lancamento.categoria.nome,
                    lancamento.tipo,
                    lancamento.id,
                ),
            )
            if cursor.rowcount == 0:
                raise LancamentoNaoEncontradoError(
                    "Lançamento nunca foi adicionado"
                )

    @staticmethod
    def _reconstituir(linha: tuple) -> Lancamento:
        id_lanc, descricao, valor, data_str, categoria_nome, tipo = linha
        categoria = Categoria(categoria_nome)
        data_obj = date.fromisoformat(data_str)
        return Lancamento.reconstituir(
            id_lanc, descricao, valor, data_obj, categoria, tipo
        )