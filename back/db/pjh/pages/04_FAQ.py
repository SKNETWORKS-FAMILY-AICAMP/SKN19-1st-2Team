"""
FAQ 페이지
제조사별 FAQ (신차 구매 시 자주 묻는 질문)
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FAQ - DOCHICHA.Inc",
    page_icon="❓"
)

def main():
    st.title("❓ FAQ")
    st.markdown("신차 구매 시 자주 묻는 질문을 확인하세요.")
    
    # 제조사 선택
    st.subheader("🏭 제조사 선택")
    
    manufacturer = st.selectbox(
        "제조사를 선택하세요",
        ["전체", "현대", "기아", "쉐보레", "르노삼성", "쌍용"]
    )
    
    # FAQ 카테고리
    st.subheader("📂 카테고리")
    
    category = st.selectbox(
        "질문 카테고리를 선택하세요",
        ["전체", "계약/구매", "납기/배송", "보증/AS", "금융/할부", "기타"]
    )
    
    # FAQ 데이터 (임시)
    faq_data = {
        "현대": [
            {
                "질문": "아반떼 구매 시 할부 조건은 어떻게 되나요?",
                "답변": "현대자동차는 다양한 할부 조건을 제공합니다. 12개월부터 60개월까지 선택 가능하며, 금리는 신용도에 따라 달라집니다.",
                "카테고리": "금융/할부"
            },
            {
                "질문": "소나타 출고까지 얼마나 걸리나요?",
                "답변": "소나타 출고는 주문 후 약 2-4주 정도 소요됩니다. 색상과 옵션에 따라 차이가 있을 수 있습니다.",
                "카테고리": "납기/배송"
            },
            {
                "질문": "현대차 보증 기간은 얼마나 되나요?",
                "답변": "현대자동차는 기본 3년/6만km 보증을 제공하며, 파워트레인은 5년/10만km 보증을 제공합니다.",
                "카테고리": "보증/AS"
            }
        ],
        "기아": [
            {
                "질문": "스포티지 구매 시 계약 절차는 어떻게 되나요?",
                "답변": "기아자동차 구매 계약은 1) 상담 및 견적 2) 계약서 작성 3) 계약금 납부 4) 출고 순으로 진행됩니다.",
                "카테고리": "계약/구매"
            },
            {
                "질문": "기아차 AS 서비스는 어디서 받을 수 있나요?",
                "답변": "전국 기아자동차 공식 서비스센터에서 AS 서비스를 받을 수 있습니다. 홈페이지에서 가까운 센터를 찾을 수 있습니다.",
                "카테고리": "보증/AS"
            }
        ]
    }
    
    # FAQ 표시
    st.subheader("💬 자주 묻는 질문")
    
    if manufacturer == "전체":
        all_faqs = []
        for brand, faqs in faq_data.items():
            for faq in faqs:
                faq["제조사"] = brand
                all_faqs.append(faq)
        
        display_faqs = all_faqs
    else:
        display_faqs = faq_data.get(manufacturer, [])
    
    # 카테고리 필터링
    if category != "전체":
        display_faqs = [faq for faq in display_faqs if faq["카테고리"] == category]
    
    # FAQ 표시
    if display_faqs:
        for i, faq in enumerate(display_faqs):
            with st.expander(f"Q{i+1}. {faq['질문']}"):
                st.markdown(f"**제조사**: {faq.get('제조사', manufacturer)}")
                st.markdown(f"**카테고리**: {faq['카테고리']}")
                st.markdown(f"**답변**: {faq['답변']}")
    else:
        st.info("선택한 조건에 해당하는 FAQ가 없습니다.")
    
    # 질문하기 섹션
    st.markdown("---")
    st.subheader("💭 궁금한 점이 있으신가요?")
    
    with st.form("question_form"):
        user_question = st.text_area("질문을 입력하세요", placeholder="궁금한 점을 자유롭게 입력해주세요.")
        user_email = st.text_input("이메일 (선택사항)", placeholder="답변을 받을 이메일 주소")
        
        submitted = st.form_submit_button("질문 제출")
        
        if submitted:
            if user_question:
                st.success("질문이 제출되었습니다! 빠른 시일 내에 답변드리겠습니다.")
            else:
                st.error("질문을 입력해주세요.")

if __name__ == "__main__":
    main()
