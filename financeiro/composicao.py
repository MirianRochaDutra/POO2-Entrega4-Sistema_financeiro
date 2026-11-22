import sqlite3
from dataclasses import dataclass

from financeiro.aplicacao.gerar_relatorio_mensal import GerarRelatorioMensal
from financeiro.aplicacao.importar_extrato import ImportarExtrato
from financeiro.aplicacao.registrar_lancamento import RegistrarLancamento
from financeiro.dominio.criador_importador import CriadorImportador
from financeiro.dominio.criador_leitor import CriadorLeitor
from financeiro.dominio.exportador_relatorio import ExportadorCSV
from financeiro.infraestrutura.esquema_sqlite import criar_esquema
from financeiro.infraestrutura.repositorio_lancamento_memoria import (
    RepositorioLancamentoMemoria,
)
from financeiro.infraestrutura.repositorio_lancamento_sqlite import (
    RepositorioLancamentoSQLite,
)


@dataclass
class Aplicacao:
    registrar_lancamento: RegistrarLancamento
    importar_extrato: ImportarExtrato
    gerar_relatorio_mensal: GerarRelatorioMensal


def montar_aplicacao(
    armazenamento: str = "sqlite",
    caminho_banco: str = ":memory:",
) -> Aplicacao:
    """Raiz de Composição: único ponto do sistema que conhece as três camadas e monta o grafo de objetos."""
    if armazenamento == "memoria":
        repositorio_lancamento = RepositorioLancamentoMemoria()
    elif armazenamento == "sqlite":
        conexao = sqlite3.connect(caminho_banco)
        criar_esquema(conexao)
        repositorio_lancamento = RepositorioLancamentoSQLite(conexao)
    else:
        raise ValueError(f"Armazenamento desconhecido: {armazenamento}")

    criador_leitor = CriadorLeitor()
    criador_importador = CriadorImportador()
    exportador = ExportadorCSV()

    return Aplicacao(
        registrar_lancamento=RegistrarLancamento(repositorio_lancamento),
        importar_extrato=ImportarExtrato(
            repositorio_lancamento, criador_leitor, criador_importador
        ),
        gerar_relatorio_mensal=GerarRelatorioMensal(
            repositorio_lancamento, exportador
        ),
    )