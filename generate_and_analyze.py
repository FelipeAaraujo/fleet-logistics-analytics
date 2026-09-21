import numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(33)
REGIOES = ["Sudeste","Sul","Nordeste","Centro-Oeste"]
MONTHS = pd.date_range("2023-01-01", "2025-12-01", freq="MS")  # 36 months

rows = []
region_params = {
    "Sudeste": {"base": 9000, "trend": 12, "amp": 700, "phase": 2},
    "Sul": {"base": 6000, "trend": 6, "amp": 950, "phase": 9},   # strong seasonal peak (agro)
    "Nordeste": {"base": 6000, "trend": 9, "amp": 500, "phase": 5},
    "Centro-Oeste": {"base": 5000, "trend": 15, "amp": 900, "phase": 8},  # agro harvest peak
}
for regiao, p in region_params.items():
    for t, month in enumerate(MONTHS):
        seasonal = p["amp"] * np.sin(2*np.pi*(month.month - p["phase"])/12)
        noise = rng.normal(0, p["amp"]*0.12)
        volume = p["base"] + p["trend"]*t + seasonal + noise
        rows.append({"regiao": regiao, "mes": month, "volume_m3": round(max(0,volume),1)})

df = pd.DataFrame(rows)
df.to_csv("/home/claude/project5/demanda_mensal_regiao.csv", index=False)

# --- Forecasting: per-region model with trend + seasonal dummies (no statsmodels available) ---
results = []
forecast_rows = []
for regiao in REGIOES:
    sub = df[df["regiao"]==regiao].reset_index(drop=True)
    sub["t"] = np.arange(len(sub))
    sub["month_num"] = sub["mes"].dt.month
    month_dummies = pd.get_dummies(sub["month_num"], prefix="m")
    X = pd.concat([sub[["t"]], month_dummies], axis=1)
    y = sub["volume_m3"]

    # backtest: train on first 30 months, test on last 6
    X_train, y_train = X.iloc[:30], y.iloc[:30]
    X_test, y_test = X.iloc[30:], y.iloc[30:]
    model = LinearRegression().fit(X_train, y_train)
    pred_test = model.predict(X_test)
    mape = (np.abs((y_test.values - pred_test)/y_test.values)).mean()*100
    results.append({"regiao": regiao, "mape_pct": round(mape,1)})

    # refit on full history, forecast next 3 months (Q1 2026)
    model_full = LinearRegression().fit(X, y)
    future_t = np.arange(len(sub), len(sub)+3)
    future_months = pd.date_range(sub["mes"].max() + pd.offsets.MonthBegin(1), periods=3, freq="MS")
    future_month_num = future_months.month
    future_dummies = pd.DataFrame({f"m_{m}": (future_month_num==m).astype(int) for m in range(1,13)})
    for col in month_dummies.columns:
        if col not in future_dummies.columns:
            future_dummies[col] = 0
    future_dummies = future_dummies[month_dummies.columns]
    Xf = pd.concat([pd.DataFrame({"t": future_t}).reset_index(drop=True), future_dummies.reset_index(drop=True)], axis=1)
    pred_future = model_full.predict(Xf)
    for m, v in zip(future_months, pred_future):
        forecast_rows.append({"regiao": regiao, "mes": m, "volume_previsto_m3": round(v,1)})

res_df = pd.DataFrame(results)
fc_df = pd.DataFrame(forecast_rows)
res_df.to_csv("/home/claude/project5/backtest_mape.csv", index=False)
fc_df.to_csv("/home/claude/project5/previsao_q1_2026.csv", index=False)

print(res_df.to_string(index=False))
print()
print(fc_df.to_string(index=False))

# fleet sizing: capacity per vehicle per month (from project1 baseline: ~25 m3 capacity, ~20 trips/month effective)
cap_m3_por_veiculo_mes = 25 * 20 * 1.0  # capacidade media * viagens utilizaveis por veiculo/mes
print(f"\nCapacidade assumida por veiculo/mes: {cap_m3_por_veiculo_mes:.0f} m3")

current_fleet_by_region = {"Sudeste":22, "Sul":13, "Nordeste":14, "Centro-Oeste":11}  # allocacao atual (soma 60, proporcional a frota real)
for regiao in REGIOES:
    vol_media_prevista = fc_df[fc_df["regiao"]==regiao]["volume_previsto_m3"].mean()
    frota_necessaria = vol_media_prevista / cap_m3_por_veiculo_mes
    atual = current_fleet_by_region[regiao]
    gap = frota_necessaria - atual
    print(f"{regiao}: previsto {vol_media_prevista:,.0f} m3/mes -> frota necessaria ~{frota_necessaria:.1f} (atual {atual}, gap {gap:+.1f})")
