# Discussão de Código e Implementação
## Conteúdo
1. ***Introducao***
2. ***Configuração do Ambiente***
3. ***Organização do Projeto***
4. ***Conceitos e Implementação***
  - Estrutura Geral
  - Repordutibilidade de Resultados
  - Vazamento de Dados
  - Pipeline Principal
  - Pipeline de Entrada de Dados
5. ***Guia de Utilização***

# Introdução

Esse guia tem como objetivo apresentar os tópicos relacionados à implementação dos modelos. **Toda implementação se baseia na linguagem de programação Python e em seus pacotes**.

Inicialmente será apresentada as etapas para correta configuração do ambiente de execução, com os detalhes das configurações testadas e pacotes utilizados. Para uma melhor compreensão das decisões de implementação e da própria modelagem dos problemas (realizada nos notebooks), será apresentada uma breve discussão conceitual de tópicos relevantes à modelagem e as respectivas implementações na seção *Conceitos e Implementação*. Por fim, será incluído um guia prático com configurações válidas e apresentação de *scripts* de procedimentos pré-definidos.

Ao final desse guia, você será capaz de:
1. Configurar um **Python virtualenv** para executar qualquer experimento apresentados nos diversos notebooks
2. Conhecer conceitos chaves utilizados nas etapas de modelagem
3. Entender a estrutura do projeto e os motivos das decisões que levaram a tal estrutura
4. Alterar configurações para a execução de novos experimentos

# Configuração do Ambiente
O projeto foi desenvolvido e testado em ambiente GNU-Linux utilizando Python 3.6. Não há dependência de hardware especializado, como GPUs, e os pacotes utilizados possuem versões para ambiente Windows.

1. O projeto requer a utilização do 3.5, ou superior, do Python
2. **Recomenda-se fortemente a utilização de embiente virtual (Python virtualenv)**
3. Os pacotes e suas versões encontram-se no arquivo *requirements.txt* encontrado na pasta raíz do projeto
4. A execução completa dos treinamentos dos modelos consomem cerca de 1GB de memória RAM

Para configuração através do virtualenv, siga o seguinte procedimento:

Abra uma janela terminal e navegue até a pasta raiz do projeto.

Verifique ou instale o pacote `virtualenv`:  
`pip install virtual`

Crie um ambiente virtual:  
`virtualenv udacity-nubank-env`

Ative o ambiente virtual criado:  

Linux:   `source udacity-nubank-env/bin/activate`  
Window:  `udacity-nubank-env\Scripts\activate`

Instale as dependências contidas no arquivo `requirements.txt`:  
`pip install -r requirements.txt`

Neste ponto, já é possível executar as rotinas de treinamento e previsão utilizando o terminal com o ambiente virtual ativo. Lembre-se re reativá-lo caso necessite mudar de terminal ou retomar a execução posteriormente

# Organização do Projeto

O projeto encontra-se organizado nos seguintes diretórios:

- ***notebook***: Contém os *notebooks* desenvolvidos na resolução dos problemas. A numeração inicial no nome dos *notebooks* indica a ordem de criação.
- ***doc***: Contém toda a documentação, incluindo os notebooks em formato PDF
- ***config***: Contém os arquivos de configuração dos três problemas (*Credit Risk*,*Customer Spending* e *Fraud Detection*)
- ***experiments***: Contém os diretórios dos três modelos onde são salvos os diversos experimentos (Diretório criado durante a rotina de treinamento)
- ***src***: Contém o código fonte do *framework* desenvolvido para a resolução dos problemas
- ***data***: Contém os dados fornecidos para o problema
- ***new_data***: Pasta utilizada para predição de novos dados. Os arquivos com as predições são salvos dentro do dirétorio `predictions`, nessa mesma pasta

## Notebooks
Os *notebooks* apresentam um ordem numérica no nome do arquivo que indica a ordem sua ordem de criação. Seguir essa ordem pode facilitar o entendimento, mas não é necessário. Cada *notebook*  é independente e apresenta uma análise do problema, das considerações iniciais até as conclusões.  
Existem dois notebook especiais: `03_classification_cv_analysis.ipynb` e `05_regression_cv_analysis.ipynb`. Estes *notebooks* são utilizados como uma forma rápida de visualização e análise dos resultados do modelo nas fases de validação cruzada e teste final de validação.

# Conceitos e Implementação
Nesta seção, serão discutidos diversos conceitos que levaram à estrutura final do projeto. Em parte, as discussões tratarão de tópicos relacionados à implementação e boas práticas de desenvolvimento e, em outros momentos, serão tratados temas relacionados diretamento com Ciência de Dados.

## Estrutura Geral
A arquitetura do projeto foi pensada de forma a alcançar um equilíbrio entre facilidade de implementação, com funções modularizadas e classes genéricas que aumentam a reusabilidade do código, e facilidade de execução de experimentos de *machine learning*.

Um problema recorrente na área de ciência dos dados é, uma vez codificado um modelo, executar diversas configurações e variações desse modelo enquanto se mantém o histórico de resultados. A solução ingênua para esse problema é a replicação de código, o que gera dificuldades de organização e manutenção.

**Neste projeto, define-se Experimento como uma configuração de um Modelo mais um conjunto de Hiperparâmetros capaz de receber um conjunto de dados e retornar um conjunto de predições e métricas de performance**. Assim, por exemplo, um experimento de regressão linear consiste na configuração do modelo (regressão linear simples, regularização, normalização de dados, etc) e um conjunto de hiperparâmetros (coeficiente de regularização, conjunto de variáveis de entrada, *feature engineering*).

A configuração de um experimento é feita através de arquivos de configuração (YAML). Nesses arquivos, definem se múltiplas seções que representam os experimentos e cada seção descreve precisamente todos os aspectos de um experimento. Cada experimento fica alocado em seu próprio diretório, com resultados, predições e *logs* enquanto uma função principal permite a execução de um conjunto arbitrário desses experimentos. Dessa forma, pode-se facilmente definir diversas configurações enquanto se mantém o histórico de performance e predições.

Cada experimento faz uso de classes padronizadas que aceitam um conjunto de configurações que controla seu comportamento. Dessa forma, o trabalho de implementação é reduzido ficando, principalmente, restrito à implementação de características ligadas diretamente ao problema que se está modelando como, por exemplo, *feature engineering*.

## Reprodutibilidade de Resultados
Outro aspecto fundamental da ciência dos dados, e da ciência em geral, diz respeito à reprodutibilidade de resultados. É indispensável que, uma vez obtidos os resultados de um experimento, eles possam ser reproduzidos pelo autor, em um momento posterior, ou por terceiros.

Neste projeto, utiliza-se a semente aleatória (*random seed*) como principal fonte de determinismo dos experimentos. É de fundamental importância que as classes implementadas para uso no framework utilizem a semente definida no arquivo de configuração do experimento.

Além disso, classes com comportamento aleatório que são utilizados em diversos objetos, como os geradores de `KFold`, são únicos e compartilhados dentro do Pipeline principal.

## Vazamento de Dados
Uma das grandes dificuldades da modelagem de problemas no framework de *machine learning* é transformar variáveis sem incorrer em vazamento de dados (*data leakage*). Vazamento de dados consiste en incluir informação do conjunto de testes ou validação no procedimento de treinamento. Utilizar esse tipo de informação no treinamento traz sérios problemas relacionados à invalidação das métricas de performance nos conjuntos de validação. Enquanto, à primeira vista, pode parecer simples evitar esse tipo de vazamento, o problema mostra-se extramente complexo quando se utiliza de técnicas de validação cruzada ou *feature engineering* que utilizam informação de multiplas observações. Note que algo simples como incluir, como dado de entrada, a média de uma variável cria um vazamento de dados se a média for tomada antes da divisão dos dados em treinamento e validação.

Diversos *frameworks* de *machine learning* apresentam arquiteturas para mitigar o vazamento de dados. Nesse projeto, foi utilizado a arquitetura do `scikit-learn`. Essa arquitetura consiste em implementar as transformações de dados em duas etapas:

1. ***Fitting phase***: Etapa de treinamento onde qualquer estatística ou transformação dos dados pode ser armazenada
2. ***Transforming phase***: Etapa onde dados, apresentando potencialmente informações de validação e teste, serão transformados. Nessa estapa, apenas estatísticas da fase de *fitting* podem ser utilizadas.

Dessa forma, todos os modelos ou classes de transformação de dados foram implementados segundo esse paradigma.

## Pipeline Principal
Tem-se `GenericPipeline` como a principal classe para execução de um experimento neste projeto. Essa classe é reponsável por executar todos os procedimentos de configuração de um experimento, seguindo um arquivo de configuração, e implementa um conjunto de ações(*actions*) que podem ser aplicados sobre o modelo:

1. ***grid_search***: Realiza a ação de busca de um conjunto ótimo de hiperparâmetros
2. ***cross_validation***: Executa o experimento com validação cruzada para análise das métricas de performance
3. ***training***: Executa o treinamento, própriamente dito, do modelo
4. ***final_validation***: Executa a validação final do modelo treinado em um conjunto de validação mantido à parte durante as etapas anteriores
5. ***prediction***: Utiliza o modelo treinado para realizar predições em novos dados

## Pipeline de Entrada de dados
A entrada de dados no modelo se dá por pipeline padronizado que recebe o conjunto completo de dados e executa seleções e transformações antes de chegar ao modelo propriamente dito.

A pilha do pipeline de entrada inicia com o recebimento do conjunto completo de dados. O primeiro conjunto de transformações da pilha diz repeito a *feature engineering*. Nesse ponto, a função de transformação tem acesso ao conjunto completo de dados e por isso há liberdade total para a criação de novas *features*. Após a etapa de *feature engineering*, o pipeline segue com a seleção de variaveis definidas em config (*column selection*). A partir daí, somente as variáveis selecionadas em config seguirão o pipeline. Nesse ponto, ele se divide em dois. As variavéis marcadas com *dtype* igual a *category*, seguem o pipeline de dados categóricos que contém a sequência de preenchimento de dados ausentes (*missing data transformer*) e uma etapa opcional de transformação final. Os dados quantitativos seguem um pipeline paralelo com transformações análogas ao pipeline categórico. Por fim as *features* são novamente unidas e seguem para o modelo.

# Guia de utilização
Nesta seção, será dado um rápido *overview* do modo de uso e configurações do *framework*.

## Scripts
No diretório raiz do projeto, encontram-se três *scripts* que podem ser utilizados para realizar as principais ações.

- `run_cross_validation.sh`: Executa o processo de validação cruzada dos três modelos e salva os resultados em seus respectivos diretórios. Os resultados podem ser visualizados com os notebooks de análise de resuldatos
- `run_full_pipeline.sh`: Realiza o processo completo.
  1. Roda a rotina de validação cruzada e salva os resultados
  2. Executa a rotina de treinamento e salva o pipeline em disco para posterior utilização
  3. Realiza a a avaliação final do modelo nos dados de validação
  4. Utiliza o pipeline salvo em disco para realizas as predições do arquivo de dados fornecido no diretório `new_data`
- `run_predict_new_data.sh`: Utiliza o modelo treinado anteriormente para realizar predições de novos dados

## Linha de comando
Toda ação dos modelos é invocada à partir do *script* `main.py`. Esse script aceita dois parâmetros de entrada:
- `-m / --model MODEL_NAME`: Seleciona o modelo para executar. Os valores possíveis são: `credit_risk`, `fraud_detection` e `customer_spending`
- `-a / --actions ACTION_NAME [opcional]`: Argumento opcional para sobrescrever a lista de *actions* do arquivo de configuração

## Arquivos de configurações
A melhor maneira de utilizar os arquivos de configuração é à partir do arquivo exemplo `sample_config.yaml`. Os arquivos utilizados nos modelos também consistituem um bom guia de utilização.
