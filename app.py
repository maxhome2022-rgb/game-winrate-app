import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="게임 플레이 시간에 따른 승률 예측", page_icon="🎮")

# 데이터의 timePlayed 단위 (Kaggle 설명에는 '시간'으로 적혀 있음)
TIME_UNIT = "시간"
MIN_MATCHES = 20  # 경기 수가 너무 적은 플레이어는 승률이 불안정해서 제외


@st.cache_data
def load_data():
    df = pd.read_csv("cod.csv")
    df["matches"] = df["wins"] + df["losses"]
    df = df[(df["matches"] >= MIN_MATCHES) & (df["timePlayed"] > 0)].copy()
    df["win_rate"] = df["wins"] / df["matches"] * 100
    return df


@st.cache_data
def fit_model(df):
    # 승률은 플레이 시간에 비례해 직선으로 오르지 않고 점점 완만해지므로
    # 플레이 시간에 log를 취해 직선(1차식)으로 학습합니다.
    x = np.log1p(df["timePlayed"])
    y = df["win_rate"]
    slope, intercept = np.polyfit(x, y, 1)
    r2 = np.corrcoef(x, y)[0, 1] ** 2
    return slope, intercept, r2


def predict_win_rate(hours, slope, intercept):
    return float(np.clip(slope * np.log1p(hours) + intercept, 0, 100))


df = load_data()
slope, intercept, r2 = fit_model(df)

st.title("게임 플레이 시간에 따른 승률 예측")
st.write("Call of Duty 플레이어 데이터를 바탕으로, 플레이 시간에 따른 예상 승률을 보여줍니다.")

st.divider()

st.subheader("플레이 시간 입력")
max_time = int(df["timePlayed"].quantile(0.99))
play_time = st.slider(
    f"게임 플레이 시간 ({TIME_UNIT})",
    min_value=1,
    max_value=max_time,
    value=int(df["timePlayed"].median()),
)

win_rate = predict_win_rate(play_time, slope, intercept)

st.divider()

st.subheader("예상 승률")
col1, col2 = st.columns(2)
col1.metric("선택한 플레이 시간", f"{play_time:,} {TIME_UNIT}")
col2.metric("예상 승률", f"{win_rate:.1f} %")
st.progress(int(win_rate))

st.divider()

st.subheader("데이터 보기")
chart_df = df[["timePlayed", "win_rate"]].rename(
    columns={"timePlayed": f"플레이 시간({TIME_UNIT})", "win_rate": "승률(%)"}
)
st.scatter_chart(chart_df, x=f"플레이 시간({TIME_UNIT})", y="승률(%)")
st.caption(
    f"분석 대상: 경기 수 {MIN_MATCHES}회 이상인 플레이어 {len(df):,}명 · "
    f"모델 설명력(R²) {r2:.2f}"
)
st.caption("※ 이 데이터에서 나타난 경향을 바탕으로 한 단순 예측이며, 실제 승률과 다를 수 있습니다.")
