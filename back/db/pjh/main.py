# main.py  (또는 현재 메인 페이지 파일 전체 교체)
import streamlit as st

st.set_page_config(
    page_title="Home - DOCHICAR",
    page_icon="🚗",
    layout="wide",
)

# ============== 스타일 ==============
st.markdown("""
<style>
/* 전체 여백 & 가독성 */
.main-container {padding: 10px 0 80px;}

/* 히어로 배너 */
.hero {
  background: linear-gradient(135deg, #FAD961 0%, #F76B1C 100%);
  border-radius: 24px;
  padding: 56px 48px;
  color: #1b1b1b;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}
.hero h1 {
  margin: 0 0 10px 0; 
  font-size: 48px; 
  font-weight: 900;
  letter-spacing: -0.02em;
}
.hero p {
  margin: 0; 
  font-size: 18px; 
  opacity: 0.9;
}

/* 섹션 공통 */
.section { margin-top: 36px; }
.section h2 { font-size: 24px; font-weight: 800; margin-bottom: 14px; }

/* 3열 카드 그리드(반응형) */
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
@media (max-width: 1100px){ .grid-3 { grid-template-columns: repeat(2, 1fr);} }
@media (max-width: 700px){ .grid-3 { grid-template-columns: 1fr; } }

/* 카드 */
.card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 18px;
  padding: 18px 18px 16px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}
.card h3 { margin: 4px 0 10px; font-size: 24px; font-weight: 800; }
.card p { margin: 0; font-size: 17px; opacity: 0.95; line-height: 1.7; }
.big-letter { font-size: 58px; font-weight: 900; color: #FAD961; text-shadow: 0 1px 2px rgba(0,0,0,0.2); }

/* 푸터 */
.footer {
  margin-top: 40px;
  opacity: 0.7;
  font-size: 13px;
  text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ============== 섹션 렌더 함수 ==============
def render_hero():
    st.markdown("""
    <div class="hero">
      <h1>도치카 DOCHICAR</h1>
      <p>도로 위 새로운 시작, 당신의 첫 차를 만나는 곳</p>
    </div>
    """, unsafe_allow_html=True)

def render_values():
    st.markdown('<div class="section"><h2>우리 서비스, 이렇게 달라요</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="grid-3">
      <div class="card">
        <div class="big-letter">도</div>
        <h3>도로 위 새 출발</h3>
        <p>처음 차를 고를 때 꼭 필요한 정보만 간결하게 보여 드립니다.</p>
      </div>
      <div class="card">
        <div class="big-letter">치</div>
        <h3>치밀한 데이터</h3>
        <p>최근 신차 중심의 가격·연료·차종·출시일 정보로 합리적인 선택을 돕습니다.</p>
      </div>
      <div class="card">
        <div class="big-letter">카</div>
        <h3>카-라이프의 즐거움</h3>
        <p>모델 열람, 비교, 정비소 찾기까지 한 곳에서 자연스럽게 이어집니다.</p>
      </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

def render_flow():
    st.markdown('<div class="section"><h2>이용 흐름</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="grid-3">
      <div class="card">
        <h3>1) 모델 열람</h3>
        <p>브랜드/차종/연료/가격으로 빠르게 필터링하며 신차를 둘러보세요.</p>
      </div>
      <div class="card">
        <h3>2) 차량 비교</h3>
        <p>관심 모델을 담아 스펙을 나란히 확인하고 중요한 차이를 발견하세요.</p>
      </div>
      <div class="card">
        <h3>3) 정비소 찾기</h3>
        <p>내 주변 서비스 센터 정보를 확인하고 방문을 준비하세요.</p>
      </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class="footer">
      © DOCHICHA.Inc · All rights reserved.
    </div>
    """, unsafe_allow_html=True)

# ============== 페이지 렌더 ==============
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    render_hero()
    render_values()
    render_flow()   # 필요 없으면 이 줄만 주석 처리
    render_footer()
    st.markdown('</div>', unsafe_allow_html=True)
