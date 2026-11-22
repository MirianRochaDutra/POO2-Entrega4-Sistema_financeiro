Sistema de Controle Financeiro Pessoal — Documentação de Arquitetura e Entregas
Visão Geral do Projeto
Este repositório contém a implementação completa do Sistema de Controle Financeiro Pessoal, desenvolvido de forma incremental ao longo dos cinco módulos da disciplina de Modelagem de Domínio em Python.
O objetivo do sistema é permitir o gerenciamento de receitas, despesas, contas e relatórios financeiros, evoluindo desde os conceitos fundamentais da Programação Orientada a Objetos (POO) até uma arquitetura em camadas totalmente desacoplada e baseada em padrões de projeto (Clean Architecture / Ports & Adapters).

1. Primeira Entrega (Módulos 1 e 2): Modelagem de Domínio e Invariantes
A primeira etapa do projeto concentrou-se na descoberta e modelagem das entidades fundamentais do domínio financeiro, estabelecendo regras de negócio rígidas e garantindo a integridade dos dados sem depender de bibliotecas externas ou frameworks.
Conceitos Orientados a Objetos Aplicados

Objetos Ricos vs. Objetos Anêmicos: As entidades do sistema possuem estado e comportamento encapsulados. Em vez de atuarem como meras estruturas de dados (DTOs) manipuladas por funções externas, classes como Conta e Lancamento contêm suas próprias validações de integridade.
Encapsulamento e Proteção de Invariantes: Uma invariante é uma regra de negócio que nunca pode ser violada. O sistema impede a criação de lançamentos sem descrição, valores zerados ou negativos, ou tipos que não sejam 'debito' ou 'credito'. A classe Conta garante que operações de débito e crédito aceitem apenas montantes positivos.
Composição vs. Associação: A relação entre Fechamento e Lancamento, assim como entre Extrato e Fechamento, foi modelada como uma composição todo-parte. A classe Fechamento é proprietária do seu conjunto de lançamentos.
Cópia Defensiva: Para evitar que coleções internas sejam mutadas externamente por código cliente, os construtores realizam cópia defensiva (self._lancamentos = list(lancamentos)) e as propriedades retornam novas listas (return list(self._lancamentos)).
Validação de Limites Temporais: A classe Fechamento valida no momento da instanciação se todos os lançamentos estão estritamente contidos no intervalo entre inicio e fim, lançando exceção caso identifique lançamentos fora do período.
Conciliação Bancária: A classe Conciliacao atua como auditora do domínio, comparando o total de débitos com o total de créditos e assegurando que a igualdade seja respeitada antes de efetivar a conciliação.

Mapeamento no Código do Projeto
Classe / MóduloCamada / ArquivoResponsabilidade do DomínioConceito de POO AplicadoCategoriafinanceiro/dominio/categoria.pyClassificação do gasto ou receitaEntidade básica com validação de nome obrigatório.Lancamentofinanceiro/dominio/lancamento.pyRegistro individual de movimentaçãoObjeto rico com invariantes de tipo, valor e descrição.Contafinanceiro/dominio/conta.pyControle de saldo e movimentaçõesEncapsulamento de saldo com operações debitar e creditar.Fechamentofinanceiro/dominio/fechamento.pyConsolidação temporal de lançamentosComposição, cópia defensiva e validação de período.Conciliacaofinanceiro/dominio/conciliacao.pyValidação de igualdade entre débitos e créditosAuditoria de invariante financeira (total_debitos == total_creditos).Extratofinanceiro/dominio/extrato.pyResumo consolidado de múltiplos fechamentosAgregação e cálculo de saldos acumulados do período.
Justificativas das Decisões de Projeto

Por que a lista de lançamentos é copiada no Fechamento?
Se o Fechamento apenas armazenasse a referência da lista recebida no construtor, uma alteração posterior nessa lista fora da classe (como um lista.clear() ou lista.append()) alteraria o estado interno do fechamento sem que ele pudesse validar as datas do novo item. A cópia defensiva garante o encapsulamento total.
Por que Conciliacao virou uma classe própria em vez de um método do Fechamento?
O Fechamento tem como responsabilidade consolidar o resumo financeiro de um período. A Conciliacao possui uma responsabilidade distinta: conferir a igualdade de saldos entre dois conjuntos específicos de lançamentos. Isolar essa regra em uma classe própria evita acoplamento e atende ao Princípio da Responsabilidade Única (SRP).
Comportamento em cenários de exceção e listas vazias:

Um Fechamento sem lançamentos é considerado válido e resulta em totais e saldo zerados.
A tentativa de instanciar um Fechamento com lançamentos fora do intervalo de datas dispara ValueError.
Executar conciliar() quando a soma dos débitos difere da soma dos créditos dispara ValueError com mensagem descritiva do saldo divergente.




2. Segunda Entrega (Módulo 3): Variação de Comportamento com Padrão Strategy
A segunda etapa introduziu a necessidade de lidar com múltiplas regras de cálculo intercambiáveis (rendimentos de investimentos, fórmulas de juros e índices de correção monetária) sem recorrer a estruturas condicionais encadeadas (if/elif).
Conceitos Orientados a Objetos Aplicados

Padrão Strategy: Encapsulamento de algoritmos de cálculo em classes separadas que compartilham uma interface comum. O objeto consumidor utiliza a estratégia sem precisar conhecer a fórmula concreta.
Interfaces e Abstração em Python: Utilização do módulo abc (ABC e @abstractmethod) para definir contratos explícitos que forçam as subclasses a implementar o método calcular(...).
Polimorfismo: Capacidade de invocar estrategia.calcular(valor) sobre diferentes instâncias e obter o comportamento específico de cada regra de forma transparente.
Princípio Open/Closed (OCP): A adição de um novo tipo de rendimento ou índice de inflação é realizada criando uma nova classe de estratégia, sem editar nenhuma linha de código das classes existentes.
Entidade com Validade Temporal: A classe OfertaRendimento demonstra a composição entre uma entidade do domínio (com código e data de validade) e uma EstrategiaRendimento.

Mapeamento no Código do Projeto
Classe / InterfaceArquivo no ProjetoRegra de Negócio / AlgoritmoPadrão AplicadoEstrategiaRendimentofinanceiro/dominio/estrategia_rendimento.pyContrato abstrato para cálculo de rendimentosStrategy (Interface)RendimentoPoupancafinanceiro/dominio/estrategia_rendimento.pyAplicação de taxa fixa de poupançaStrategy ConcretaRendimentoCDBPreFixadofinanceiro/dominio/estrategia_rendimento.pyAplicação de taxa contratada de CDBStrategy ConcretaEstrategiaJurosfinanceiro/dominio/estrategia_juros.pyContrato abstrato para juros sobre capital e tempoStrategy (Interface)JurosSimplesfinanceiro/dominio/estrategia_juros.pyCálculo $C + (C \times i \times t)$Strategy ConcretaJurosCompostosfinanceiro/dominio/estrategia_juros.pyCálculo $C \times (1 + i)^t$Strategy ConcretaEstrategiaCorrecaoMonetariafinanceiro/dominio/estrategia_correcao_monetaria.pyContrato abstrato para correção por inflaçãoStrategy (Interface)CorrecaoIPCA / CorrecaoINPCfinanceiro/dominio/estrategia_correcao_monetaria.pyCorreção baseada em índices oficiais de inflaçãoStrategy ConcretaOfertaRendimentofinanceiro/dominio/oferta_rendimento.pyOferta com validade que encapsula uma estratégiaComposição de Objetos
Justificativas das Decisões de Projeto

Por que criar três interfaces separadas (EstrategiaRendimento, EstrategiaJuros e EstrategiaCorrecaoMonetaria) em vez de uma única interface genérica?
Apesar de todas realizarem cálculos matemáticos, os conceitos possuem assinaturas e semânticas de negócio distintas. EstrategiaRendimento e EstrategiaCorrecaoMonetaria operam sobre um único montante inicial (valor: float), enquanto EstrategiaJuros necessita de três parâmetros operacionais (capital: float, taxa: float, tempo: int). Forçar uma única interface geraria parâmetros não utilizados e violaria o Princípio da Segregação de Interfaces (ISP).
Estratégia armazenada em atributo vs. recebida por parâmetro:

Na OfertaRendimento, a estratégia é armazenada como atributo de instância, pois a oferta é contratada e vinculada a um produto específico com prazo de validade.
Nos métodos de simulação financeira, a estratégia é enviada como parâmetro de método, permitindo que o mesmo valor seja testado contra diferentes regras de cálculo sem alterar o estado do objeto consumidor.




3. Terceira Entrega (Módulo 4): Isolamento da Criação de Objetos e Injeção de Dependências
A terceira etapa tratou do problema da instanciação de objetos. À medida que o sistema passou a suportar diferentes leitores de arquivos (.csv, .json), múltiplos layouts bancários (BancoX, BancoY) e relatórios em variados formatos (CSV, HTML), a responsabilidade de decidir o que instanciar foi isolada usando padrões de criação.
Conceitos Orientados a Objetos Aplicados

Simple Factory: Centralização da decisão de instanciação em uma classe dedicada quando a escolha é determinada por um identificador simples (como uma extensão de arquivo ou nome de banco).
Factory Method: Padrão utilizado quando a criação faz parte de um fluxo de classe base (método-molde) e a decisão do tipo de objeto concreto a ser produzido é delegada para as subclasses.
Template Method: A classe ExportadorRelatorio define a estrutura padrão do relatório (exportar()) e delega a instanciação do documento específico para o método abstrato criar_documento().
Injeção de Dependências (DI): A classe de serviço deixa de instanciar diretamente seus colaboradores e passa a recebê-los totalmente construídos em seu método construtor __init__.
Raiz de Composição: Centralização do grafo de montagem da aplicação na função montar_aplicacao(), garantindo que o restante do sistema dependa apenas de abstrações.
Dublês de Teste (Fakes): Substituição de colaboradores reais por objetos simulados (LeitorFake, CriadorLeitorFake, CriadorImportadorFake, ExportadorFake) na suíte de testes de serviço, provando o baixo acoplamento da arquitetura.

Mapeamento no Código do Projeto
Classe / EstruturaArquivo no ProjetoFunção no SistemaPadrão / Conceito AplicadoLeitor / LeitorCSV / LeitorJSONfinanceiro/dominio/leitor.pyLeitura e parsing de arquivos físicosAbstração de LeituraCriadorLeitorfinanceiro/dominio/criador_leitor.pyInstanciação do leitor correto por extensãoSimple FactoryImportador / ImportadorBancoXfinanceiro/dominio/importador.pyAdequação do layout bancárioAbstração de ImportaçãoCriadorImportadorfinanceiro/dominio/criador_importador.pyInstanciação do importador pelo nome do bancoSimple FactoryExportadorRelatoriofinanceiro/dominio/exportador_relatorio.pyEstruturação e geração de relatóriosTemplate Method & Factory MethodExportadorCSV / ExportadorHTMLfinanceiro/dominio/exportador_relatorio.pyProdução de DocumentoCSV ou DocumentoHTMLImplementação de Factory MethodServicoImportacaofinanceiro/dominio/servico_importacao.pyOrquestração do fluxo de importaçãoInjeção de Dependênciasmontar_aplicacaofinanceiro/dominio/aplicacao.pyPonto central de instanciação do sistemaRaiz de Composição
Justificativas das Decisões de Projeto

Por que leitores e importadores usam Simple Factory, enquanto exportadores usam Factory Method?

Leitores e Importadores: A decisão sobre qual classe instanciar depende exclusivamente de uma string simples (como ".csv" ou "banco_x"). Não há fluxo comportamental compartilhado antes da criação, tornando a Simple Factory a solução mais enxuta.
Exportadores de Relatório: A classe base ExportadorRelatorio executa todo o fluxo de formatação do relatório (exportar()), mas necessita de um tipo específico de documento para adicionar as linhas. O Factory Method (criar_documento()) permite que o algoritmo da classe base permaneça inalterado enquanto as subclasses decidem se constroem um DocumentoCSV ou um DocumentoHTML.


O que é injetado e o que é criado internamente no ServicoImportacao?

Injetado: Os colaboradores duradouros (criador_leitor, criador_importador e exportador) entram pelo construtor.
Criado Internamente: Os objetos transientes do fluxo de dados (como Fechamento e Extrato) são instanciados durante a execução do método importar(), pois seus dados dependem da leitura do arquivo no momento da chamada.




4. Quarta Entrega (Módulo 5): Arquitetura em Camadas, Persistência e Inversão de Dependências
A quarta e última etapa do projeto reestruturou o sistema segundo os princípios da Clean Architecture (Arquitetura Hexagonal / Ports & Adapters). As regras de negócio foram isoladas do acesso a dados, os serviços monolíticos foram divididos em Casos de Uso, e foi introduzido o padrão Repository com suporte à persistência real em banco de dados SQLite.
Conceitos Orientados a Objetos Aplicados

Identidade e Reconstituição de Entidades: A classe Lancamento recebeu uma identidade estável (_id: int | None) atribuída no momento em que é salva no repositório. Para reler registros do banco sem reexecutar validações de criação, foi adicionado o construtor alternativo @classmethod reconstituir(...).
Padrão Repository: A interface RepositorioLancamento define as operações de coleção do domínio (adicionar, obter, listar e atualizar). As implementações concretas tratam o armazenamento sem vazar detalhes técnicos para o domínio.
Persistência Relacional em SQLite: A classe RepositorioLancamentoSQLite traduz os objetos do domínio em tabelas relacionais com controle transacional rigoroso (with self._conexao).
Casos de Uso (Application Services): Divisão das intenções do usuário em classes focadas de responsabilidade única (RegistrarLancamento, ImportarExtrato, GerarRelatorioMensal).
Arquitetura em Camadas:

dominio/: Núcleo contendo entidades, validações, estratégias e contratos de repositório. Não possui nenhuma dependência externa.
aplicacao/: Casos de uso que orquestram o fluxo entre entidades e repositórios.
infraestrutura/: Implementações concretas de banco de dados (SQLite, Memória) e scripts DDL.


Princípio de Inversão de Dependências (DIP): As camadas internas (Domínio e Aplicação) definem suas portas/contratos. A camada externa (Infraestrutura) adapta-se a esses contratos.
Raiz de Composição Única: O arquivo financeiro/composicao.py atua como a única fronteira que conhece todas as camadas e injeta os repositórios adequados na função montar_aplicacao(armazenamento="sqlite" | "memoria").
Testes de Arquitetura: Validações estáticas em test_arquitetura.py utilizando o módulo ast para garantir que o pacote dominio/ nunca importe módulos da aplicacao/ ou infraestrutura/.

Mapeamento Completo da Estrutura de Diretórios
financeiro/
├── __init__.py
├── composicao.py                         <-- Raiz de Composição (Junta todas as camadas)
├── dominio/                              <-- CAMADA DE DOMÍNIO (Regras Puras e Contratos)
│   ├── __init__.py
│   ├── categoria.py                      (Entidade Categoria)
│   ├── lancamento.py                     (Entidade Lançamento com ID e Reconstituição)
│   ├── conta.py                          (Entidade Conta)
│   ├── fechamento.py                     (Consolidação de Período)
│   ├── conciliacao.py                    (Auditoria Débito = Crédito)
│   ├── extrato.py                        (Relatório do Extrato)
│   ├── estrategia_rendimento.py          (Padrão Strategy)
│   ├── estrategia_juros.py               (Padrão Strategy)
│   ├── estrategia_correcao_monetaria.py (Padrão Strategy)
│   ├── oferta_rendimento.py              (Entidade com Validade)
│   ├── leitor.py                         (Abstração de Leitura)
│   ├── criador_leitor.py                 (Simple Factory)
│   ├── importador.py                     (Abstração de Importação)
│   ├── criador_importador.py             (Simple Factory)
│   ├── exportador_relatorio.py           (Factory Method & Template Method)
│   └── repositorio_lancamento.py         (Contrato/Interface do Repositório)
├── aplicacao/                            <-- CAMADA DE APLICAÇÃO (Casos de Uso)
│   ├── __init__.py
│   ├── registrar_lancamento.py           (Caso de Uso: Criar e Persistir Lançamento)
│   ├── importar_extrato.py               (Caso de Uso: Ler Extrato e Salvar no Repositório)
│   └── gerar_relatorio_mensal.py         (Caso de Uso: Consultar e Exportar Relatório)
└── infraestrutura/                       <-- CAMADA DE INFRAESTRUTURA (Persistência)
    ├── __init__.py
    ├── esquema_sqlite.py                 (DDL / Criação de Tabelas SQLite)
    ├── repositorio_lancamento_memoria.py (Repositório para Testes Rápidos)
    └── repositorio_lancamento_sqlite.py  (Repositório Relacional em Banco SQLite)

tests/                                    <-- SUÍTE COMPLETA DE TESTES AUTOMATIZADOS
├── __init__.py
├── conftest.py                           (Fixtures Parametrizadas: Memória e SQLite)
├── test_categoria.py                     (Testes de Categoria)
├── test_conta.py                         (Testes de Conta)
├── test_lancamento.py                    (Testes de Lançamento)
├── test_fechamento.py                    (Testes de Fechamento)
├── test_conciliacao.py                   (Testes de Conciliação)
├── test_extrato.py                       (Testes de Extrato)
├── test_estrategia_rendimento.py         (Testes de Estratégia de Rendimento)
├── test_estrategia_juros.py              (Testes de Estratégia de Juros)
├── test_estrategia_correcao_monetaria.py(Testes de Correção Monetária)
├── test_oferta_rendimento.py             (Testes de Oferta)
├── test_leitor.py                        (Testes de Leitura)
├── test_criador_leitor.py                (Testes da Factory de Leitor)
├── test_importador.py                    (Testes de Importador)
├── test_criador_importador.py            (Testes da Factory de Importador)
├── test_exportador_relatorio.py          (Testes de Exportação)
├── test_repositorio_lancamento.py        (Testes de Contrato do Repositório)
├── test_persistencia_sqlite.py           (Testes de Sobrevivência ao Reinício em Disco)
├── test_casos_de_uso.py                  (Testes dos Casos de Uso de Aplicação)
├── test_composicao.py                    (Testes da Raiz de Composição)
└── test_arquitetura.py                   (Testes Automatizados de Inviolabilidade das Camadas)

Justificativas das Decisões de Projeto

Por que usar o padrão Repository em vez de acessar o SQLite diretamente nos serviços?
O acoplamento direto com o SQLite impediria a realização de testes unitários em memória e prenderia a aplicação a uma tecnologia específica de banco de dados. O padrão Repository cria uma "coleção emulado na memória", permitindo que os Casos de Uso trabalhem apenas com objetos Lancamento sem saber como eles são persistidos.
O que foi decidido não persistir nesta etapa e por quê?
Optou-se por persistir prioritariamente a entidade Lancamento no banco relacional SQLite. Entidades dinâmicas e transientes, como Fechamento, Conciliacao e Extrato, são calculadas sob demanda pelos Casos de Uso no momento da consulta a partir dos lançamentos persistidos. Isso evita redundância de dados e problemas de dessincronização no banco de dados.
Como a suíte de testes garante que ambas as implementações do repositório cumprem o mesmo contrato?
Utilizou-se uma fixture parametrizada em tests/conftest.py que executa a mesma suíte de testes de test_repositorio_lancamento.py duas vezes consecutivas: uma vez para RepositorioLancamentoMemoria e outra para RepositorioLancamentoSQLite. Isso valida na prática o Princípio da Substituição de Liskov (LSP).
O que mudaria se o SQLite fosse substituído por um ORM (como SQLAlchemy)?
Graças ao desacoplamento da arquitetura:

A camada de dominio/ e a camada de aplicacao/ não sofreriam nenhuma alteração.
Apenas seria criada uma nova classe RepositorioLancamentoORM dentro da camada de infraestrutura/.
Na Raiz de Composição (composicao.py), bastaria atualizar a instanciação do repositório.




Como Executar o Projeto e os Testes Automatizados
Pré-requisitos

Python 3.10 ou superior.
Gerenciador de pacotes pip.

Configuração do Ambiente no Windows (PowerShell)
# 1. Ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1

# 2. Instalar as dependências do projeto
pip install -r requirements.txt

# 3. Executar a suíte completa de testes automatizados
pytest -v


Conclusão
A evolução do Sistema de Controle Financeiro Pessoal demonstra na prática como princípios de Orientação a Objetos, Padrões de Projeto e Arquitetura em Camadas trabalham juntos para criar um código robusto, testável e sustentável a longo prazo.