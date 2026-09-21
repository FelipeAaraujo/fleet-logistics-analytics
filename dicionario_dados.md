# Dicionário de Dados — Projeto 1: Fleet & Logistics Analytics

Base 100% sintética, gerada por script Python, simulando 12 meses (jan–dez/2025) de operação
de uma frota fictícia de 60 caminhões-tanque de transporte de combustíveis ("RotaViva Logística").

## veiculos.csv (60 registros)
| Campo | Tipo | Descrição |
|---|---|---|
| id_veiculo | texto | Identificador único do veículo (VEI-001 a VEI-060) |
| regiao | texto | Região de operação (Sudeste, Sul, Nordeste, Centro-Oeste) |
| ano_fabricacao | inteiro | Ano de fabricação do veículo |
| capacidade_m3 | inteiro | Capacidade volumétrica do tanque, em m³ |

## viagens.csv (21.719 registros)
| Campo | Tipo | Descrição |
|---|---|---|
| id_viagem | texto | Identificador único da viagem |
| id_veiculo | texto | Chave estrangeira para veiculos.csv |
| regiao | texto | Região da viagem |
| data_viagem | data | Data da viagem |
| km_rodado | decimal | Quilômetros rodados na viagem |
| litros_combustivel | decimal | Litros de diesel consumidos |
| custo_combustivel | decimal (R$) | Custo do combustível na viagem |
| custo_pedagio | decimal (R$) | Custo de pedágio na viagem |
| volume_m3 | decimal | Volume transportado, em m³ |
| faturamento_viagem | decimal (R$) | Faturamento gerado pela viagem |
| tempo_carregamento_min | decimal | Tempo de carregamento, em minutos |
| tempo_descarga_min | decimal | Tempo de descarga, em minutos |
| disponibilidade_mes_veiculo | decimal (0–1) | Disponibilidade do veículo no mês da viagem |

## manutencoes.csv (112 registros)
| Campo | Tipo | Descrição |
|---|---|---|
| id_manutencao | texto | Identificador único do evento de manutenção |
| id_veiculo | texto | Chave estrangeira para veiculos.csv |
| data | data | Data do evento de manutenção |
| tipo | texto | preventiva ou corretiva |
| custo_manutencao | decimal (R$) | Custo do evento de manutenção |

## Relacionamentos
- veiculos (1) → viagens (N) via id_veiculo
- veiculos (1) → manutencoes (N) via id_veiculo

## Principais resultados calculados sobre esta base
- Disponibilidade média da frota: 93,8%
- Custo de manutenção total da frota: R$ 679.218,55
- 9 dos 60 veículos (15% da frota) respondem por 45,2% do custo total de manutenção, com
  disponibilidade média de 90,4% (gap de 3,4 p.p. frente à frota)
- Economia estimada ao nivelar esses 9 veículos ao custo mediano dos demais: R$ 251.541,56/ano
  (37% do custo total de manutenção)
- Custo por km médio da frota: R$ 2,06
