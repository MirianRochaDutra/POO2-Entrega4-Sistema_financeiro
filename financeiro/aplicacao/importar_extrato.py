from financeiro.dominio.criador_importador import CriadorImportador
from financeiro.dominio.criador_leitor import CriadorLeitor
from financeiro.dominio.lancamento import Lancamento
from financeiro.dominio.repositorio_lancamento import RepositorioLancamento


class ImportarExtrato:
    """Caso de uso: ler arquivo de extrato bancário e persistir os lançamentos importados."""

    def __init__(
        self,
        repositorio_lancamento: RepositorioLancamento,
        criador_leitor: CriadorLeitor,
        criador_importador: CriadorImportador,
    ) -> None:
        self._repositorio = repositorio_lancamento
        self._criador_leitor = criador_leitor
        self._criador_importador = criador_importador

    def executar(
        self,
        caminho: str,
        extensao: str,
        banco: str,
    ) -> list[Lancamento]:
        leitor = self._criador_leitor.criar(extensao)
        lancamentos_lidos = leitor.ler(caminho)

        importador = self._criador_importador.criar(banco)
        lancamentos_importados = importador.importar(lancamentos_lidos)

        for lancamento in lancamentos_importados:
            self._repositorio.adicionar(lancamento)

        return lancamentos_importados