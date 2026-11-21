# Model Card · PedalHora

## Modelo e finalidade

Rede neural densa de regressão, construída com Keras e TensorFlow. A saída linear estima o total de aluguéis no sistema Capital Bikeshare para uma hora. A aplicação limita o valor inferior a zero e arredonda para o inteiro mais próximo.

**Uso previsto:** simulação acadêmica de demanda horária histórica na rede Capital Bikeshare, para ilustrar como estimativas podem orientar o planejamento operacional.

## Dados e entradas

Fonte: [Bike Sharing, UCI](https://doi.org/10.24432/C5W894), licenciado em CC BY 4.0. O arquivo horário cobre 2011–2012. As entradas são hora, mês, dia da semana, indicador de dia útil, temperatura, umidade, vento e condição do tempo. Hora e mês têm uma representação cíclica. A hora e o dia da semana também entram como indicadores. A condição rara de tempo severo é agrupada à precipitação.

O alvo é `cnt`. As variáveis `casual` e `registered` foram excluídas por conterem os componentes do alvo. A camada de normalização usa exclusivamente as estatísticas de treino. A interface usa os divisores documentados no arquivo original da UCI (41, 100 e 67).

## Treinamento e avaliação

Treino, validação e teste são blocos cronológicos contíguos (~60/20/20%). Treinamos três arquiteturas com Adam e perda MAE. O early stopping acompanha a perda de validação, com paciência de 12 épocas e restauração dos melhores pesos. A seleção usa o menor MAE de validação, e as métricas de teste são calculadas após a seleção. A referência simples é a mediana histórica por hora e tipo de dia. A árvore de decisão é uma comparação adicional.

Rede selecionada na validação: **96 × 48 neurônios**. Teste final: 3.476 registros horários, de 07/08/2012 a 31/12/2012.

| Modelo | MAE de teste (aluguéis/hora) |
| --- | ---: |
| Baseline | 116,63 |
| Árvore de decisão | 104,35 |
| Rede Keras | 89,27 |

**Frase de negócio.** No período de teste, a PedalHora estimou o total de aluguéis da rede com erro médio de 89,27 aluguéis por hora, uma redução de 23,5% no erro da regra histórica.

## Limitações

- O período histórico é curto, com dados de uma única rede. A demanda pode mudar com expansão, preços, novos hábitos e disponibilidade de bicicletas.
- A avaliação usa o clima observado. Uma aplicação futura que dependa de previsão meteorológica pode apresentar erro maior.
- A demanda observada pode estar limitada pela disponibilidade de bicicletas. O modelo aprende a prever aluguéis registrados.
- O MAE resume o erro médio do conjunto. A estimativa por hora não tem intervalo de confiança e pode ter erro maior em picos, feriados e mau tempo.
- A previsão é agregada. A base usada não permite estimar a demanda por estação.

## Não usar para

Tomar decisões automáticas de redistribuição de bicicletas em produção, estabelecer orçamento de operação, prever demanda em cidades brasileiras ou estimar demanda atual sem revalidação, nem recomendar a disponibilidade de uma estação específica.
