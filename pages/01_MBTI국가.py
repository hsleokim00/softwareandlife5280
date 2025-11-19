# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

st.set_page_config(
    page_title="세계 MBTI 분포 대시보드",
    layout="wide"
)

@st.cache_data
def load_data():
    # 같은 폴더에 countriesMBTI_16types.csv 파일이 있다고 가정
    csv_path = "countriesMBTI_16types.csv"
    if not os.path.exists(csv_path):
        # Streamlit Cloud에서 에러 메시지로 안내
        st.error(
            "❌ 'countriesMBTI_16types.csv' 파일을 찾을 수 없습니다.\n"
            "앱이 있는 폴더에 CSV 파일을 함께 업로드해 주세요."
        )
        return None
    df = pd.read_csv(csv_path)
    return df

df = load_data()
if df is None:
    st.stop()

st.title("🌍 국가별 MBTI 유형 분포 대시보드")
st.markdown(
    "국가를 선택하면 해당 국가의 **MBTI 16유형 비율**을 "
    "**인터랙티브한 Plotly 막대그래프**로 확인할 수 있어요.\n\n"
    "🔴 **1등(가장 비율이 큰 유형)은 빨간색**, 나머지는 **그라데이션 컬러**로 표시됩니다."
)

# ----- 사이드바: 국가 선택 -----
with st.sidebar:
    st.header("국가 선택")
    countries = df["Country"].sort_values().tolist()
    selected_country = st.selectbox("Country", countries, index=countries.index("Korea, South") if "Korea, South" in countries else 0)
    st.markdown("---")
    st.caption("📁 데이터: countriesMBTI_16types.csv")

# ----- 데이터 준비 -----
mbti_cols = df.columns[1:]  # 첫 컬럼은 Country
row = df[df["Country"] == selected_country].iloc[0]
values = row[mbti_cols].values

data_df = pd.DataFrame({
    "MBTI": mbti_cols,
    "Ratio": values
})

# ----- 색상 설정: 1등 빨간색 + 나머지 그라데이션 -----
max_idx = data_df["Ratio"].idxmax()
max_val = data_df.loc[max_idx, "Ratio"]

# 그라데이션용 팔레트 (Blues 계열)
palette = px.colors.sequential.Blues

min_val = data_df["Ratio"].min()
max_other_val = data_df["Ratio"].max()
value_range = max_other_val - min_val if max_other_val != min_val else 1e-9

colors = []
for i, v in enumerate(data_df["Ratio"]):
    if i == max_idx:
        # 1등은 빨간색
        colors.append("#FF4136")
    else:
        # 값에 따라 0~1로 정규화
        frac = (v - min_val) / value_range
        # 팔레트 인덱스 선택
        idx = int(frac * (len(palette) - 1))
        colors.append(palette[idx])

# ----- Plotly 막대그래프 생성 -----
fig = go.Figure(
    data=[
        go.Bar(
            x=data_df["MBTI"],
            y=data_df["Ratio"],
            marker=dict(color=colors),
            hovertemplate="<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>",
        )
    ]
)

fig.update_layout(
    title=f"📊 {selected_country} MBTI 유형 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    yaxis_tickformat=".0%",
    bargap=0.2,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)

# ----- 메인 화면 출력 -----
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader(f"{selected_country} 데이터")
    st.dataframe(
        data_df.sort_values("Ratio", ascending=False).reset_index(drop=True),
        use_container_width=True
    )
    st.caption("⬆ 1등 MBTI는 빨간색으로 표시됩니다.")
