# front/pages/05_FAQ.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="FAQ - DOCHICHA.Inc", page_icon="❓", layout="wide")

st.markdown("""
<style>
h1 { font-size: 2.1rem; font-weight: 900; }
h2 { font-size: 1.35rem; font-weight: 800; }
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p { font-size: 1.02rem; line-height: 1.6; }
div[data-testid="stExpander"] button { font-size: 1.02rem; }
.small-dim { opacity: .8; }
</style>
""", unsafe_allow_html=True)

def exclude_escalation(faqs: list[dict]) -> list[dict]:
    if not faqs: return []
    ban = ["문의", "1:1", "콜센터", "상담", "전화", "챗봇", "고객센터", "센터로", "연락"]
    def bad(text: str) -> bool:
        t = (text or "")
        return any(w in t for w in ban)
    out = []
    for f in faqs:
        q, a = f.get("질문", ""), f.get("답변", "")
        if bad(q) or bad(a):
            continue
        out.append(f)
    return out

def main():
    st.title("❓ FAQ")
    st.markdown("신차 구매 시 자주 묻는 질문을 확인하세요.")

    st.subheader("🏭 제조사 선택")
    manufacturer = st.selectbox("제조사를 선택하세요", ["전체", "현대", "기아", "쉐보레", "르노코리아", "KG 모빌리티"])

    st.subheader("📂 카테고리")
    category = st.selectbox("질문 카테고리를 선택하세요", ["전체", "계약/구매", "납기/배송", "보증/AS", "금융/할부", "기타"])

    # 임시 데이터 (입력 순서 = 인기순)
    faq_data = {
        "현대": [
            {"질문": "보유차를 팔고 싶은데 어떻게 하나요?",
             "답변": "현대 인증중고차 ‘내차팔기’에서 온라인 접수 후 차량 점검/가격 산정/거래까지 원스톱 진행할 수 있습니다.",
             "카테고리": "기타"},
            {"질문": "블루멤버스 포인트는 어디에 사용할 수 있나요?",
             "답변": "차량 구매 시 현금처럼 사용(개인/개인사업자 기준 최대 400만P) 가능하며 주유·충전·쇼핑 등 제휴처에서도 사용/적립할 수 있습니다.",
             "카테고리": "금융/할부"},
            {"질문": "친환경 폐차 절차는 어떻게 진행되나요?",
             "답변": "홈페이지에서 친환경 폐차 서비스를 신청하면 회수·해체·재활용까지 절차가 안내됩니다. 조기폐차는 지자체 확인·보조금 신청이 추가됩니다.",
             "카테고리": "기타"},
            {"질문": "차량 구매 시 카드 결제는 어느 정도 가능하나요?",
             "답변": "현금/카드/할부/포인트 조합이 가능하며 카드 가능 한도는 차종·프로모션·카드 상품 조건에 따라 달라집니다.",
             "카테고리": "금융/할부"},
            {"질문": "계약 후 예상 납기일은 어디서 확인하나요?",
             "답변": "차종별 안내 페이지에서 일반 납기 정보를 제공하며, 계약 고객은 마이페이지의 ‘계약상세’에서 본인 계약 건의 상태를 확인할 수 있습니다.",
             "카테고리": "납기/배송"},
        ],
        "기아": [
            {"질문": "스포티지 구매 계약은 어떻게 진행되나요?",
             "답변": "상담 및 견적 → 계약서 작성 → 계약금 납부 → 출고 순으로 진행됩니다.",
             "카테고리": "계약/구매"},
            {"질문": "기아차 보증/AS 기준은 어떻게 되나요?",
             "답변": "차종/부품별로 상이하나 기본 보증, 파워트레인 보증 등 항목별 정책이 제공됩니다.",
             "카테고리": "보증/AS"},
        ],
        "쉐보레": [
            {"질문": "TOP10 FAQ는 어떤 항목인가요?",
             "답변": "자주 찾는 핵심 질문 10개를 선별해 빠르게 확인할 수 있도록 구성되어 있습니다.",
             "카테고리": "기타"},
        ],
        "르노코리아": [
            {"질문": "정비 관련 기본 가이드는 어디서 볼 수 있나요?",
             "답변": "공식 사이트의 차량 관리/정비 안내에서 기본 점검 항목과 가이드를 확인할 수 있습니다.",
             "카테고리": "보증/AS"},
        ],
        "KG 모빌리티": [
            {"질문": "KGM LINK 서비스에서 가능한 기능은?",
             "답변": "디지털키, 원격제어, 차량상태 확인 등 커넥티드 기능을 제공합니다.",
             "카테고리": "기타"},
        ],
    }

    if manufacturer == "전체":
        all_faqs = []
        for brand, faqs in faq_data.items():
            for f in faqs:
                f = f.copy()
                f["제조사"] = brand
                all_faqs.append(f)
        display = all_faqs
    else:
        display = [dict(x, 제조사=manufacturer) for x in faq_data.get(manufacturer, [])]

    display = exclude_escalation(display)
    if category != "전체":
        display = [f for f in display if f.get("카테고리") == category]

    st.subheader("💬 자주 묻는 질문")
    if display:
        for i, faq in enumerate(display, start=1):
            with st.expander(f"Q{i}. {faq['질문']}"):
                st.markdown(f"**제조사**: {faq.get('제조사','-')}  \n**카테고리**: {faq['카테고리']}")
                st.markdown(faq["답변"])
    else:
        st.info("선택한 조건에 해당하는 FAQ가 없습니다.")

    st.markdown("---")
    st.subheader("💭 추가로 궁금한 점이 있나요?")
    with st.form("faq_q_form"):
        question = st.text_area("질문을 입력하세요", placeholder="궁금한 점을 자유롭게 입력해주세요.")
        email = st.text_input("이메일 (선택)")
        submitted = st.form_submit_button("질문 제출")
        if submitted:
            if question.strip():
                st.success("질문이 제출되었습니다!")
            else:
                st.error("질문을 입력해주세요.")

if __name__ == "__main__":
    main()
