import streamlit as st

# 기본 설정
st.set_page_config(
    page_title="베스킨라빈스 키오스크",
    page_icon="🍨",
    layout="centered",
)

st.title("🍨 베스킨라빈스 키오스크")
st.caption("천천히 선택해 주세요! 제가 친절하게 도와드릴게요 😊")

# -----------------------------
# 1. 매장/포장 선택
# -----------------------------
st.markdown("### 1️⃣ 이용 방법을 선택해 주세요")

eat_type = st.radio(
    "매장에서 드시나요, 포장해 가시나요? 🏠👜",
    ["매장 식사 🍽️", "포장해 갈래요 🛍️"],
    horizontal=True,
)

# -----------------------------
# 2. 용기 선택
# -----------------------------
st.markdown("---")
st.markdown("### 2️⃣ 아이스크림 용기를 골라 주세요")

containers = {
    "싱글컵 (1스쿱)": {"max_scoops": 1, "price": 3500},
    "더블컵 (최대 2스쿱)": {"max_scoops": 2, "price": 6500},
    "파인트 (최대 3스쿱)": {"max_scoops": 3, "price": 9500},
    "쿼터 (최대 4스쿱)": {"max_scoops": 4, "price": 13500},
}

container_name = st.selectbox(
    "용기를 선택해 주세요 🥣",
    list(containers.keys()),
)

selected_container = containers[container_name]
max_scoops = selected_container["max_scoops"]
base_price = selected_container["price"]

st.info(
    f"✅ **{container_name}** 선택! "
    f"최대 **{max_scoops}스쿱**까지 담을 수 있어요. (이하로 선택 가능) 😉"
)

# -----------------------------
# 3. 맛 선택 (용기 스쿱 수 이하로)
# -----------------------------
st.markdown("---")
st.markdown("### 3️⃣ 아이스크림 맛을 골라 주세요")

flavors = [
    "엄마는외계인 👽",
    "슈팅스타 💫",
    "민트초코 💚",
    "뉴욕치즈케이크 🧀",
    "아몬드봉봉 🥜",
    "바람과 함께 사라지다 🌪️",
    "초콜릿 무스 🍫",
    "레인보우 샤베트 🌈",
    "쿠키앤크림 🍪",
    "스트로베리 🍓",
]

num_scoops = st.slider(
    "몇 스쿱 담을까요? (1 ~ 최대값 이하로 선택 가능) 🍧",
    min_value=1,
    max_value=max_scoops,
    value=max_scoops,
    help="용기 최대 스쿱 수 이하로만 선택할 수 있어요!",
)

selected_flavors = []
for i in range(num_scoops):
    flavor = st.selectbox(
        f"{i+1}번 스쿱 맛을 골라 주세요 😋",
        flavors,
        key=f"flavor_{i}",
    )
    selected_flavors.append(flavor)

# -----------------------------
# 4. 결제 방법 선택 및 최종 가격
# -----------------------------
st.markdown("---")
st.markdown("### 4️⃣ 결제 방법을 선택해 주세요")

pay_method = st.radio(
    "어떤 방법으로 결제하시나요? 💳💵",
    ["카드 결제 💳", "현금 결제 💵"],
    horizontal=True,
)

# 결제 금액 (여기서는 용기별 고정 금액만 사용)
final_price = base_price

st.markdown("### 5️⃣ 주문 확인 & 결제")

if st.button("✅ 주문 완료하기"):
    st.success("주문이 접수되었습니다! 아래 내용을 한 번 더 확인해 주세요 😊")

    st.subheader("🧾 주문 내역")

    # 이용 방식
    st.write("**이용 방식:**", eat_type)

    # 용기 정보
    st.write("**용기:**", container_name)

    # 맛 정보
    st.write("**선택한 스쿱 수:**", f"{num_scoops} 스쿱")
    st.write("**선택한 맛들:**")
    for idx, f in enumerate(selected_flavors, start=1):
        st.write(f"- {idx}번 스쿱: {f}")

    # 결제 정보
    st.write("**결제 방법:**", pay_method)

    # 최종 금액
    st.markdown(
        f"### 💰 최종 결제 금액: **{final_price:,.0f}원**"
    )
    st.caption("맛있게 드시고, 오늘도 달콤한 하루 보내세요 🍦✨")
else:
    st.info("아이스크림 선택이 끝나셨다면 **‘주문 완료하기’** 버튼을 눌러 주세요 😄")
