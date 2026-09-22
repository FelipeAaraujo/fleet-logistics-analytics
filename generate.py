import numpy as np, pandas as pd
rng = np.random.default_rng(42)

N_VEH = 60
REGIONS = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste"]
MONTHS = pd.date_range("2025-01-01", "2025-12-01", freq="MS")

# vehicle master data with a hidden "quality" factor driving cost/availability
veiculos = pd.DataFrame({
    "id_veiculo": [f"VEI-{i:03d}" for i in range(1, N_VEH+1)],
    "regiao": rng.choice(REGIONS, N_VEH),
    "ano_fabricacao": rng.integers(2014, 2024, N_VEH),
    "capacidade_m3": rng.choice([20, 25, 30, 36], N_VEH),
})
quality = rng.beta(5, 2, N_VEH)  # 0-1, higher = better condition
veiculos["_quality"] = quality

trip_rows = []
maint_rows = []
maint_id = 1
for _, v in veiculos.iterrows():
    q = v["_quality"]
    for month in MONTHS:
        n_trips = max(0, int(rng.normal(25 + 8*q, 4)))
        # unavailability days this month (worse quality -> more downtime)
        downtime_days = max(0, rng.normal((1-q)*6, 1.5))
        disponibilidade_mes = max(0, 1 - downtime_days/30)
        # maintenance events, more likely for low quality vehicles
        if rng.random() < (0.06 + (1-q)*0.35):
            custo_manut = float(rng.normal(3800 + (1-q)*6000, 900))
            custo_manut = max(300, custo_manut)
            maint_rows.append({
                "id_manutencao": f"MNT-{maint_id:04d}",
                "id_veiculo": v["id_veiculo"],
                "data": month + pd.Timedelta(days=int(rng.integers(0, 27))),
                "tipo": rng.choice(["preventiva", "corretiva"], p=[0.4, 0.6]),
                "custo_manutencao": round(custo_manut, 2),
            })
            maint_id += 1
        for t in range(n_trips):
            km = max(50, rng.normal(340, 90))
            km_l = max(1.6, rng.normal(2.6 + q*1.1, 0.25))  # worse quality => lower km/l
            litros = km / km_l
            preco_diesel = 6.1
            custo_combustivel = litros * preco_diesel
            custo_pedagio = km * rng.uniform(0.15, 0.35)
            volume_m3 = min(v["capacidade_m3"], max(8, rng.normal(v["capacidade_m3"]*0.8, 4)))
            faturamento = km * rng.uniform(11, 15) * (volume_m3 / v["capacidade_m3"])
            tempo_carreg = max(15, rng.normal(55 - 10*q, 12))
            tempo_desc = max(15, rng.normal(48 - 8*q, 10))
            trip_rows.append({
                "id_viagem": f"{v['id_veiculo']}-{month.strftime('%Y%m')}-{t:03d}",
                "id_veiculo": v["id_veiculo"],
                "regiao": v["regiao"],
                "data_viagem": month + pd.Timedelta(days=int(rng.integers(0, 27))),
                "km_rodado": round(km, 1),
                "litros_combustivel": round(litros, 1),
                "custo_combustivel": round(custo_combustivel, 2),
                "custo_pedagio": round(custo_pedagio, 2),
                "volume_m3": round(volume_m3, 1),
                "faturamento_viagem": round(faturamento, 2),
                "tempo_carregamento_min": round(tempo_carreg, 1),
                "tempo_descarga_min": round(tempo_desc, 1),
                "disponibilidade_mes_veiculo": round(disponibilidade_mes, 3),
            })

viagens = pd.DataFrame(trip_rows)
manutencoes = pd.DataFrame(maint_rows)
veiculos = veiculos.drop(columns=["_quality"])

viagens.to_csv("/home/claude/project1/viagens.csv", index=False)
manutencoes.to_csv("/home/claude/project1/manutencoes.csv", index=False)
veiculos.to_csv("/home/claude/project1/veiculos.csv", index=False)

print("viagens:", len(viagens), "manutencoes:", len(manutencoes), "veiculos:", len(veiculos))
