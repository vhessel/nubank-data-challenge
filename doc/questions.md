# Data Challenge 2018 - Nubank

- [Introdução](#introduçao)
  - [Sobre o Nubank](#sobre-o-nubank)
  - [O Processo de aprovação](#o-processo-de-aprovacao)
  - [Fraudes](#fraudes)
- [Tarefas](#tarefas)
  - [Análise Exploratória](#analise-exploratoria)
  - [Modelagem](#modelagem)
    - [Risco de Crédito](#risco-de-credito)
	- [Propensão a gasto](#propensa-a-gasto)
	- [Fraude](#fraude)
  - [Resolvendo um problema de negócio](#resolvedo-um-problema-de-negocio)
- [Entregáveis](#entregaveis)
- [O que esperamos das equipes?](#o-que-esperamos-das-equipes)
- [Arquivos](#arquivos)
- [Os dados](#os-dados)

## Introdução

### Sobre o Nubank

#### Somos inconformados
No Brasil, pagamos as tarifas e os juros mais altos do mundo pelos piores serviços bancários. Nós sabemos que tecnologia e design podem resolver esse problema.

Por isso, nos unimos em 2013 para redefinir a relação das pessoas com o dinheiro, através de uma experiência mais eficiente e transparente.

Nosso objetivo é acabar com a complexidade e devolver o controle da vida financeira para cada um.

#### Somos diferentes

Somos uma startup que desenvolve soluções simples, seguras e 100% digitais para você ter o controle do seu dinheiro literalmente nas suas mãos.

Somos NUs - justos e transparentes na conduta, diretos e objetivos na comunicação, e tratamos cada cliente como uma pessoa.

Somos contra burocracia, papelada, agências e centrais de atendimento caras e ineficientes.

Somos a favor de ouvir e valorizar a sua opinião, e de merecer a sua confiança como cliente.

### O processo de aprovação

Para receber o seu cartão tudo o que o cliente precisa fazer é solicitá-lo através de um convite de um amigo ou se inscrevendo no nosso site. Após isso, nosso objetivo é responder em alguns segundos ou aprovando o cartão de crédito ou enviando o cliente para uma lista de espera. Todo esse processo faz uso pesado de Machine Learning para a tomada de decisões.
Resumidamente, o processo funciona mais ou menos assim:
 - Cliente recebe um convite ou faz sua solicitação direto pelo site do Nubank
- Nós fazemos requisições de dados nos nossos parceiros e rodamos diversos modelos
- Com os resultados em mãos tomamos uma decisão de crédito.
	- Aprovar ou não o cliente
	- Atribuir um limite de crédito inicial

### Fraudes

Embora haja verificação de documentos, existem casos de fraude. Os tipos mais comuns são de pessoas se passando por outras. Ou seja, o cartão é feito utilizando um documento, mas a pessoa que usa de fato é outra. O esperado nestes casos é que o fraudador em algum momento não pagará a sua fatura e, por ter registrado o cartão em outro nome, estará livre das cobranças, negativações e consequências da inadimplência. Um sub conjunto desses fraudadores é chamado de "Amigos & Familiares" pela alta frequência com que isso acontece entre pessoas que se conhecem e da própria família. Como há má intenção, pode-se considerar que o fraudador irá causar um prejuízo igual ao limite que lhe foi dado.

## Tarefas

### Análise Exploratória

1. Como dito, a inadimplência é o aspecto mais sensível quando se fala em crédito. Faça três visualizações que explorem a inadimplência na base fornecida.

2. Faça uma análise dos casos de fraude. Qual a relação deles com os casos de inadimplência?

3. Analisando a distribuição do volume de compras em 3 meses dos clientes (variável pv_3m), você diria que ela segue uma distribuição normal? Há algo de estranho nela? Se sim, qual seria a justificativa ou hipótese para tal?

### Modelagem

Será preciso construir três modelos. Para cada modelo deve-se entregar os arquivos responsáveis pelo treino e previsão, um csv contendo as previsões para o conjunto de teste e gerar um pdf que contenha as seguintes informações:

- O que se está tentando prever?
- Qual foi o target (variável alvo) escolhido? Se optou-se por um modelo não supervisionado, qual o motivo?
- Quais variáveis foram selecionadas e qual foi o critério de seleção?
- Quais as variáveis mais importantes do seu modelo?
- Quais métricas foram selecionadas para a validação do modelo? O que cada uma delas significa de acordo com o contexto do que se está tentando prever? Quais evidências te fariam crer ou não de que a performance de validação será a mesma de quando este modelo estiver rodando de fato com novos dados?

#### Risco de Crédito

Faça um modelo para prever o risco de inadimplência de um cliente utilizando apenas dados de acquisição, ou seja, apenas dados que são conhecidos na fase de aplicação deste. Lembre-se que o limite inicial é definido após o cliente ser aceito.

#### Propensão a Gasto

Faça um modelo que seja capaz de distinguir clientes de acordo com a sua propensão de gasto. Você é livre para transformar esse problema em regressào, classificação, não supervisionado e etc, contanto que ao final consiga distinguir qual cliente tende a gastar mais.

#### Fraude

Nós temos marcadas algmas contas como fraude de amigos & familiares ou como fraude de identificação. Faça um modelo para identificar possíveis fraudadores. Você é livre para tratar como classificação binária, multi-classe, não supervisionado e etc, mas é preciso dar uma probabilidade da pessoa ser um fraudador.  

### Resolvendo um problema de negócio


Embora tenha-se falado um pouco sobre validação na etapa anterior, até agora falamos apenas do comportamento de modelos isolados e não de decisões.

Um negócio é feito de decisões e é preciso definir como os dados serão usados para ajudar na tomada de decisão. Apesar de termos contruído três modelos até aqui, o intuito é apenas um: como decidir quais novos clientes aceitar? Para tal são tomadas duas decisões, na verdade: a aprovação do crédito e o limite inicial que será dado.

Você pode encontrar mais sobre o funcionamento do nubank em [nosso site](https://nubank.com.br/perguntas/) na seção "Sobre o Nubank". É importante salientar que não há uma resposta única e correta para este problema e que ele pode ser abordado de diferentes formas. Sinta-se livre para propor qualquer solução que você acredite ser a melhor.

Sabemos que é um problema complexo e adoraríamos ver abordagens simples, racionais e criativas.

Para a sua análise, considere as seguintes informações (elas não precisam ser obrigatoriametne usadas em sua solução):


|           Métrica                            |Valor |
|:--------------------------------------------:|:----:|
|          Taxa de juros do rotativo           |  17% |
|          Taxa de intercâmbio                 |  5%  |
|            Custo unitário do cartão          |  10  |
|Custo por minuto do serviço de atendimento    |  2.5 |
|           Inflação mensal                    | 0.5% |


A maneira com a qual esses valores relacionam-se com o negócio é a seguinte:

- Taxa de juros do rotativo: os clientes tem a opção de pagar apenas 10% de suas faturas e rolar a dívida para o próximo mês, exemplo: em uma fatura de $1000, paga-se 10% ($100) e rola $900 ($1000 - $100). A próxima fatura será $900 * (1 + 0.17) = $900 (balanço rolado) + $153 (juros do rotativo).

- Taxa de intercâmbio: é cobrado do vendedor 5% do montante total de uma compra feita por um cliente. Por exemplo, o cliente compra uma TV por $1000 e isso trará uma renda de $50 ao Nubank.

- Custo unitário do cartão: é o valor gasto para manufaturar e enviar o cartão para o cliente.

- Custo por minuto do serviço de atendimento: é o valor médio gasto por minuto que o cliente usa o serviço de atendimento.

- Inflação: é a variação média mensal no preço de uma determinada cesta de bens.


**Considerações**:
- se um cliente incorreu em inadimplência, você pode considerar que a soma do montante da última fatura mais o balanço do rotativo do último mês é a quantidade que nós perderemos com aquele cliente. Exemplo: o $900 + $153 citado acima;
- se um cliente é fraudador, ele dará um prejuízo igual ao limite de crédito concedido.

Há total liberdade para usar como bem entender os modelo que foram feitos na etapa anterior. Para responder essas perguntas deve ser feita uma apresentação na qual é discutida a abordagem, como ela foi validada, as premissas, utilização dos dados históricos e etc. Além disso, deve ser entregue:

- O código utilizado;
- Um csv com a definição de aprovado ou não e com qual linha de crédito inicial para o conjunto de teste;
- Uma apresentação em pdf que descreva a sua abordagem.

Tenha em mente que esta apresentação deve convencer executivos a adotarem a sua abordagem.

## Arquivos

- `questions.md`: este arquivo, contém as questões que devem ser respondidas;
- `rubric.md`: orientações do que é esperado e quais critérios serão usados;
- /data
  - `acquisition_train.csv`: dados de aquisição, informações que sabemos das pessoas no momento que elas aplicam, contém o target de default e fraude;
  - `acquisition_test.csv`: dados de aquisição, mas sem as variáveis alvo de default e fraude;
  - `spend_train.csv`: dados comportamentais dos clientes do conjunto de treino;
  - `sample_default_submission.csv`: arquivo exemplo de como devem ser entregues as previsões do modelo para previsão de default;
  - `sample_fraud_submission.csv`: arquivo exemplo de como devem ser entregues as previsões do modelo para previsão de fraude;
  - `sample_spending_submission.csv`: arquivo exemplo de como devem ser entregues as previsões do modelo para previsão da propensão a gasto;
  
Perceba que não há um `spend_test.csv`, pois você deve prever o comportamento de gasto dos clientes utilizando dados de acquisição na parte da modelagem e para o problema final deve definir qual seria o limite inicial deles.

## O que esperamos das equipes?

Espera-se que a equipe saiba alocar o tempo de maneira inteligente considerando que o principal item deste desafio é resolver o problema final. Todos os itens anteriores podem compor ou não esta solução final, mas esperamos que cada um deles faça com que vocês levantem considerações interessantes para a última questão.

Além disso, em todo o material produzido para as respostas, lembre-se: seja objetivo! Pense em uma audiência com pessoas de diferentes formações e entendimento do contexto do problema.

Para saber mais objetivamente o que é esperado em cada tarefa leia a rubrica, que encontra-se no arquivo `rubric.md`.

## Entregáveis

Portanto, deverá ser entegue:

- **Parte I**
  - Um pdf com o resultado da análise exploratória;
  - O código, relatório em pdf e as previsões em csv para o conjunto de teste (separar em uma pasta diferente para cada um dos três modelos);
- **Parte II**
  - O código, apresentação em pdf e a previsão em csv para o conjunto de teste.

Consulte a rubrica para maiores detalhes.

## Os dados

**ATENÇÃO**: Os dados aqui seguem o formato dos dados reais que utilizamos no Nubank. Isso significa que boa parte das variáveis possuem significado e valores iguais às que lidamos diariamente. Porém, como esses dados são sobre informações pessoais, nenhum dos dados são referentes a pessoas reais.

Há 2 tipos de dado sobre os clientes: acquisição e comportamento:

- `acquisition_train.csv` e `acquisition_test.csv` são os conjuntos de treino e teste com os dados de acquisição, neles você encontrará os targets para default (inadimplência) e fraud;
- `spends_train.csv` e `spends_test.csv`: contém o comportamento dos usuários pelos seus gastos;


### Dados de acquisição

Coluna|Tipo|Descrição
---|---|---
ids|String|identificador único de um aplicante
email|String|Provedor de e-mail do solicitante
tags|String|Tags descritivas dadas pelo provedor de dados
score_1|String|Score de crédito 1, categorias
score_2|String|Score de crédito 2, categorias
score_3|Float|Score de crédito 3
score_4|Float|Score de crédito 4
score_5|Float|Score de crédito 5
score_6|Float|Score de crédito 6
risk_rate|Float|Risco associado ao aplicante
last_amount_borrowed|Float|Valor do último empréstimo que o aplicante tomou
last_borrowed_in_months|Int\Duração do último empréstimo que o aplicante tomou
reason|String|Razão pela qual foi feita uma consulta naquele cpf
income|Float|Renda estimada pelo provedor dos dados para o aplicante
facebook_profile|Bool|Se o aplicante possui perfil no Facebook
state|String|Estado de residência do aplicante
zip|String|Código postal do aplicante
shipping_zip_code|Int|Código do endereço de entrega
shipping_state|String|Estado do endereço de entrega
channel|String|Canal pelo qual o aplicante aplicou
job_name|String|Profissão do aplicante
real_state|String|Informação sobre habitação do aplicante
ok_since|Float|Quantidade de dias que
n_bankruptcies|Float|Quantidade de bancarrotas que o aplicante já experimentou
n_defaulted_loads|Float|Quantidade de empréstimos não pagos no passado
n_accounts|Float|Número de contas que o aplicante possui
n_issues|Float|Número de reclamações de terceiros feitas em alguma das contas do aplicante
user_agent|String|Informação sobre dispositivo usado para a aplicação
reported_income|Int|Renda informada pelo próprio aplicante
profile_phone_number|String|Número de telefone, ex: `210-2813414`
marketing_channel|String| Canal de marketing pelo qual o aplicante chegou na página de pedido de crédito
lat_lon|Object|Latitude e longitude da localização
external_data_provider_fraud_score|Int|Score de fraude
external_data_provider_first_name|String|Primeiro nome do aplicante
external_data_provider_email_seen_before|String|Se o e-mail já foi consultado junto ao provedor de dados
external_data_provider_credit_checks_last_year|Int|Quantidade de consultas de crédito na janela de um ano
external_data_provider_credit_checks_last_month|Int|Quantidade de consultas de crédito na janela de um mês
external_data_provider_credit_checks_last_2_year|Int|Quantidade de consultas de crédito na janela de dois anos
application_time_in_funnel|Int|Tempo gasto pelo aplicante durante o processo de aplicação
application_time_applied|Date|Horário de aplicação
target_default|Bool|Indicativo de default
target_fraud|String|Pode assumir dois valores positivos referentes a dois tipos de fraude: `fraud_id`/`fraud_friends_family`, NaN se não houve

### Dados de comportamento

Coluna|Tipo|Descrição
---|---|---
ids|String|identificador único de um aplicante
credit_line|Int|Limite do cartão
month|Int|Ordenação dos meses que a pessoa é cliente, sendo 0 o primeiro mês dela como cliente
spend|Float|Valor gasto naquele mês
revolving_balance|Float|Valor que o cliente não pagou da fatura atual e que irá rolar para a próxima
card_request|Int|Se o cliente solicitou uma nova via do cartão (ou a primeira)
minutes_cs|Float|Quantidade de minutos utilizados do serviço de atendimento ao consumidor
