# Fleet & Logistics Analytics

**Excel/Power Query → SQL → Power BI — identificando quais veículos da frota dão prejuízo**

## Contexto
A RotaViva Logística (transportadora fictícia de combustíveis) opera 60 caminhões-tanque em 4
regiões do Brasil. A gestão "sente" que a frota está subutilizada, mas não sabe apontar quais
veículos, especificamente, geram o problema.

## Problema de negócio
Identificar veículos improdutivos, custos elevados e baixa disponibilidade — e transformar isso em
recomendação de manutenção/realocação.

## Base de dados (gerada para este projeto)
- **21.719 viagens**, 60 veículos, 112 eventos de manutenção, 12 meses (jan–dez/2025).
- Arquivos: `veiculos.csv`, `viagens.csv`, `manutencoes.csv`.
- Dicionário de dados completo em `dicionario_dados.md`.

## Tratamento dos dados
Cálculo de custo por km, custo por m³, margem por viagem e índice de disponibilidade a partir dos
dados brutos de viagem e manutenção.

## Análise
Quais veículos têm custo por km acima da média da frota? Existe relação entre manutenção
recorrente e baixa disponibilidade?

## Resultado (calculado sobre a base gerada, não estimado)
- **9 dos 60 veículos (15% da frota) respondem por 45,2% do custo total de manutenção** da frota,
  com disponibilidade média de **90,4%** contra **93,8%** da frota — um gap real de 3,4 p.p.
- Se esses 9 veículos caíssem ao custo de manutenção mediano dos demais 51, a economia estimada é
  de **R$ 251.541,56/ano (37% do custo total de manutenção da frota)**.
- Custo por km médio da frota: R$ 2,06.

## Recomendação
Priorizar manutenção preventiva ou substituição desses 9 veículos; realocar rotas mais longas para
os veículos de maior disponibilidade.

## Ferramentas
Excel/Power Query (exploração inicial) → SQL (agregações) → Power BI (dashboard executivo).

## Competências demonstradas
Tratamento de dados, modelagem simples, SQL, DAX, storytelling executivo, KPIs operacionais.
