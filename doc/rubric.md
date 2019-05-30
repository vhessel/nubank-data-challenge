# Rubrica

Aqui estão descritos os aspectos que serão avaliados nas entregas pedidas para o desafio.

## Geral

- É fornecida toda a informação necessária para rodar os arquivos entregues (versões das bibliotecas e etc);
- O código fornecido roda e segue boas práticas;
- O código possui comentários;
- Todas as visualziações criadas possuem título, identificação dos eixos e outras informações necessárias para seu entendimento;
- Os relatórios são bem escritos e bem organizados.

### Manipulação dos dados

Foi capaz de...
- ler, manipular e criar visualizações com os dados fornecidos;
- identificar e comunicar todos os problemas presentes no dataset e contorná-los para os diversos usos que fez deles;
- documentar os passos realizados para limpar os dados antes do seu uso em modelos e análises;

### Exploração dos dados e análise de dados

- O conjunto de dados é explorado de várias formas. São utilizadas técnicas de análise univariada, bivariada e multivariada para explorar aspectos esperados presentes no conjunto fornecido;
- Questionamentos e observações são levantas ao longo da exploração, seja para posterior análise ou simples levantamente de hipóteses, o que inclui a interpretação de cada gráfico gerado;
- Em conformidade com o item anterior, toda visualização deve possuir um propósito ao ser feita e uma conclusão deve ser tirada do seu resultado;

### Modelos

A entrega dos modelos consiste em um arquivo de previsão em csv para cada um deles e um relatório / apresentação em pdf.

O arquivo csv com as previsões deve ter os seguintes formatos:

#### Modelo de default

| ids | default |
|---|---|
| 810e3277-619e-3154-7ba0-ebddfc5f7ea9  | 0.0356 |
| b4118fd5-77d5-4d80-3617-bacd7aaf1a88  | 0.7890 |

Ou seja, o arquivo csv deveria ser:

```
ids,default
810e3277-619e-3154-7ba0-ebddfc5f7ea9,0.0356
b4118fd5-77d5-4d80-3617-bacd7aaf1a88,0.7890

```

#### Modelo de fraude

| ids | fraud |
|---|---|
| 810e3277-619e-3154-7ba0-ebddfc5f7ea9  | 0.0190 |
| b4118fd5-77d5-4d80-3617-bacd7aaf1a88  | 0.0012 |

Ou seja, o arquivo csv deveria ser:

```
ids,fraud
810e3277-619e-3154-7ba0-ebddfc5f7ea9,0.0190
b4118fd5-77d5-4d80-3617-bacd7aaf1a88,0.0012

```

#### Modelo de gastos

| ids | spend |
|---|---|
| 810e3277-619e-3154-7ba0-ebddfc5f7ea9  | 3201 |
| b4118fd5-77d5-4d80-3617-bacd7aaf1a88  |  120 |

Ou seja, o arquivo csv deveria ser:

```
ids,spend_score
810e3277-619e-3154-7ba0-ebddfc5f7ea9,3201
b4118fd5-77d5-4d80-3617-bacd7aaf1a88,120

```

**ATENÇÃO**: Caso adote uma abordagem que gere outros tipos de previsão, lembre-se de informar o que significam as previsões que foram feitas.

O relatório deve conter (use como um checklist!):

#### Informações básicas
- Um nome para identificá-lo :)
- O modelo é reprodutível?
- O objetivo do modelo está bem definido?
- As razões para a utilização de um modelo para esse problema são razoáveis?
- A variável alvo (target) está bem definida?
- O momento em que o modelo deve rodar para um novo exemplo está bem definido?

#### Verificação dos dados

- Todas as variáveis (features) utilizadas estão listadas? Há informação sobre o quão importante cada uma delas é para o modelo?
- A estratégia para tratar dados faltantes está clara e faz sentido?
- O tamanho do conjunto de treinamento é informado e é razoável?
- Há análise descritiva para o problema que está sendo resolvido?
- Seleção de variáveis foi feita?

#### Modelo / Desempenho
- A técnica e esquema de validação escolhido é cuidadosamente explicada e justificada entre as alternativas;
- O efeito das features criadas é comprovado;
- É feito o afinamento de hiper parâmetros;
- São utilizadas e justificadas as métricas de performance
- Tais métricas são levantadas para todos os sub conjuntos utilizados
- É feita a conexão entre as métricas de performance do modelo e métricas de negócio

#### Monitoramento
- Uma estratégia de monitoramento da performance do modelo é apresentada e pontos de possíveis falhas são levantados;

#### Extras
- Adição de outras informações que não as listadas acima e que contribuam para o entendimento do funcionamento e performance dos modelos entregues;

### Desafio final
- O problema é apresentado, analisado e objetivamente tratado;
- O uso ou não dos modelos anteriormente desenvolvidos na solução final é justificado;
- Todas as premissas necessárias para o funcionamento da solução estão expostas;
- É capaz de apresentar o problema claramente, contextualizá-lo e apresentar a solução de forma amigável mesmo para pessoas sem conhecimento prévio deste (ou seja, alguém que não leu o enunciado consegue entender);
- São elaboradas e justificadas métricas a serem usadas para validar a solução final;
- É entregue um arquivo csv contendo a decisão de aprovação e limite inicial para os dados do conjunto de teste.

O csv deve seguir o formato:

| ids | approve | limit
|---|---|---|
| 810e3277-619e-3154-7ba0-ebddfc5f7ea9  | 1 | 1200
| b4118fd5-77d5-4d80-3617-bacd7aaf1a88  | 0 | NaN

Entendemos que podem haver premissas para a definição dessa resposta. Pode-se assumir alguma
### Como ir além?
- Adicionar ao relatório dos modelos visualizações que permitam interpretar os seus resultados e entender o porquê de suas previsões;
- Para a parte de modelagem, ser capaz de testar sistematicamente uma variedade considerável de modelos e abordagens;
- Criatividade e inovação na criação de novas características (features) para os modelos;
- Ser capaz de definir bons benchmarks para os modelos e solução final;
- Demonstrar mais de uma alternativa para a solução do desafio final e ser capaz de compará-las, principalemnte de maneira quantitativa;
- Considerar a complexidade dos modelos e soluções propostos e não apenas a sua performance;

### Entregas
- Foram entregues todos os arquivos requisitados e de forma organizada
- Os arquivos de previsão estão no formato correto e contém apenas as colunas requisitadas;
- Todos os relatórios e a apresentação estão em `pdf`;
- O código possui instruções para ser executado e qualquer pessoa que possua os arquivos do desafio consegue rodar e gerar o resultado final;
