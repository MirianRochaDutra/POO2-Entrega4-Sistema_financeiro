import ast
from pathlib import Path

RAIZ = Path(__file__).parent.parent / "financeiro"


def _camadas_importadas(camada: str) -> set[str]:
    importadas: set[str] = set()
    pasta = RAIZ / camada
    if not pasta.exists():
        return importadas

    for arquivo in pasta.rglob("*.py"):
        conteudo = arquivo.read_text(encoding="utf-8")
        no_ast = ast.parse(conteudo)
        for no in ast.walk(no_ast):
            if isinstance(no, ast.ImportFrom) and no.module:
                partes = no.module.split(".")
                if partes == "financeiro" and len(partes) > 1:
                    importadas.add(partes[1])
    return importadas


class TestArquitetura:

    def test_dominio_nao_conhece_outras_camadas(self) -> None:
        importadas = _camadas_importadas("dominio")
        assert "aplicacao" not in importadas
        assert "infraestrutura" not in importadas

    def test_aplicacao_nao_conhece_infraestrutura(self) -> None:
        importadas = _camadas_importadas("aplicacao")
        assert "infraestrutura" not in importadas