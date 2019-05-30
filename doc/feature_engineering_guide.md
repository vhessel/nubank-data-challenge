# Guia de Variáveis Criadas

## Nota Inicial
Este guia tem por objetivo apresentar as variáveis que foram criadas no decorrer da modelagem dos problemas. Algumas variáveis criadas acabaram por não ser utilizadas.

## Variáveis pré-processadas
Algumas variáveis foram criadas ou modificadas à partir de procedimentos de pré-processamento simples. O objetivo de tais mudanças foi o aumento de usabilidade das variáveis:

- `log_income`: log-transformação da variável `income`
- `log_reported_income`: log-transformação da variável `reported_income`
- `log_credit_limit`: log-transformação da variável `credit_limit`
- `log_last_amount_borrowed`: log-transformação da variável `last_amount_borrowed`


- `lat`: componente de latitude da variável `lat_lon`
- `lon`: componente de longitude da variável `lat_lon`
- `estimated_state`: Estado estimado à partir de `lat` e `lon`
- `estimated_district`: Município estimado à partir de `lat` e `lon`


- `application_time_applied`: Modificada para um valor numérico representando o número de minutos à partir da meia noite
- `shortned_user_agent`: Variável `user_agent` sem o número final de release de navegador
- `shipping_state_zip_code`: Valores de `shipping_state` e `shipping_zip_code` concatenados
- `shipping_zip_code`: Modificado para conter apenas os primeiros dois números da variável


- `profile_is_cellphone`: Teste de verificação se o quarto número de telefone é um dígito 9
- `profile_phone_number_ddd`: Modificado para conter apenas os primeiros dois número da variável


- `estimated_gender`: Teste de verificação se a última letra da variável `external_data_provider_first_name` é um caractere a
- `estimated_is_female`: Estimação de gênero através da variável `external_data_provider_first_name`, utilizando-se uma base parcial de nomes do Censo IBGE 2010
- `name_size`: Número de caracteres da variável `external_data_provider_first_name`

## Variáveis baseadas em aggregação
Algumas variáveis tiverams seus valores agregados dentro de conjuntos formados por outras variáveis. Esses valores agregados foram utilizados para a criação de um Z-Score, onde o valor de cada observação tem a média descontada e temina por ser dividida pelo desvio padrão dos valores do grupo ao qual ela pertence.  
Vamos a um exemplo prático. Nós criamos uma agregação da variável `income` contra a coluna `state`. Isso significa com formamos grupos de valores de `income` em cada valor da variável `state`. Calculamos a média e o desvio padrão dos valores de `income` dentro de cada grupo. Por fim, tomamos uma observação com valor específico de `income` e que pertence que tem valor de `state` igual ao de algum dos grupos que agregamos. Pegamos seu valor de `income` e subtraímos a média do grupo ao queal a observação pertence. Dividimos o resultado pelo desvio padrão do mesmo grupo e temos uma observação da nova variável Z-Score.  
Abaixo segue a lista do nome das variáveis criadas, qual variável foi agregada e qual foi o conjunto agregante:

| Nome | Agregado | Agregante |
|:---:|:----:|:-----:|
| `zscore_state_income` |`income`|`state`|
| `zscore_score_3_income` |`score_3`|`state`|
| `zscore_score_4_income` |`score_4`|`state`|
| `zscore_score_5_income` |`score_5`|`state`|
| `zscore_score_6_income` |`score_6`|`state`|
| `zscore_risk_rate_income` |`risk_rate`|`state`|
| `zscore_credit_limit_income` |`credit_limit`|`state`|
| `zscore_app ... id_income` |`application_time_applied`|`state`|
| `zscore_lat_income` |`lat`|`state`|
| `zscore_lon_income` |`lon`|`state`|
| `zscore_las ... wed_income` |`last_amount_borrowed`|`state`|
| `zscore_ex ... re_income` |`external_data_provider_email_seen_before`|`state`|
| `zscore_state_real_state_income` |`income`|`state`,`real_state`|
| `zscore_ex ... re_email` |`external_data_provider_email_seen_before`|`email`|
| `zscore_income_facebook_profile` |`income`|`facebook_profile`|
| `zscore_income_user_agent` |`income`|`user_agent`|

## Variáveis de distância
Utilizando os valores da média de latitude e longitude dentro da variáveç `state`, foram criadas 3 novas variávies:
- `distance_state`: Proxy de distância entre a coordenada geográfica da observação e a coordenada média dentro do `state` que a obsevação pertence
- `distance_state_lat`: Mesma concepção anterior mas apenas para a variável de latitude
- `distance_state_lat`: Mesma concepção anterior mas apenas para a variável de longitude

## Variáveis transformadas e de interação
Criou-se variáveis à partir da interações de duas ou mais outras variáveis e, também, de suas potências

- `score_3_squared`: Potência de ordem dois da variável `score_3` descontado sua média
- `score_4_squared`: Potência de ordem dois da variável `score_4` descontado sua média
- `score_5_squared`: Potência de ordem dois da variável `score_5` descontado sua média
- `score_6_squared`: Potência de ordem dois da variável `score_6` descontado sua média
- `income_squared`: Potência de ordem dois da variável `income` descontado sua média


-  `score_3_times_score_6`: Multiplicação da variável `score_3` pela variável `score_6`
-  `score_4_times_score_6`: Multiplicação da variável `score_4` pela variável `score_6`
-  `score_5_times_score_6`: Multiplicação da variável `score_5` pela variável `score_6`
- `reported_income_times_income`: Multiplicação da variável `reported_income` pela variável `income`


- `score_3_sum2_score_4`: Soma do quadrado da variável `score_3`, descontada sua média, com o quadrado da variável `score_4`, descontada sua média
- `score_3_sum2_score_6`: Soma do quadrado da variável `score_3`, descontada sua média, com o quadrado da variável `score_6`, descontada sua média
- `score_4_sum2_score_6`: Soma do quadrado da variável `score_4`, descontada sua média, com o quadrado da variável `score_6`, descontada sua média


- `credit_limit_per_income`: Divisão da variável `credit_limit` pela variável `income`
- `credit_limit_per_borrow`: Divisão da variável `credit_limit` pela variável `last_amount_borrowed`


- `credit_limit_minus_reported_income`: Subtração da variável `credit_limit` pela variável `reported_income`
- `reported_income_minus_income`: Subtração da variável `income` pela variável `reported_income`

## Variáveis de PCA
Utilizou-se PCA para reduzir algumas variáveis com siginificado semelhante
- `score_pca_1`, ... , `score_pca_5`: % primeiras componentes principais das variáveis de *score* de crédito `score_3`, ... , `score_6` e das variáveis de suas interações `score_3_squared`, ... ,`score_6_squared`, `score_3_times_score_6`, `score_3_times_score_6`, `score_5_times_score_6`.
