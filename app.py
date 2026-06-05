import streamlit as st
from google import genai
from google.genai import types

# 1. 페이지 설정
st.set_page_config(page_title="AI 기반 SDGs 아이디어 평가 시스템", page_icon="🧠", layout="centered")

# --- 🚀 디자인 초고도화: SF 테크 및 SDGs 감성 스타일 (CSS) ---
advanced_css = """
<style>
/* 1. 사이트 전체 배경: 우주와 지구 느낌의 고급스러운 어두운 배경 */
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.75)), 
                      url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1920");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* 2. 중앙 메인 컨테이너: 은은하게 빛나는 유리창(Glassmorphism) 효과 */
.block-container {
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    padding: 3.5rem;
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    margin-top: 3rem;
    color: #FFFFFF !important;
}

/* 3. 입력창 및 선택 상자 디자인 테두리 밝게 강조 */
div[data-baseweb="select"], div[data-baseweb="input"] {
    background-color: rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}
input {
    color: #FFFFFF !important;
}
label, p {
    color: #E5E7EB !important;
    font-weight: 500 !important;
}

/* 4. 버튼 디자인: 마우스를 올리면 네온 빛이 나는 하이테크 버튼 */
.stButton>button {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: white !important;
    border-radius: 14px !important;
    border: none !important;
    padding: 0.75rem 2rem !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
    transition: all 0.3s ease !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6) !important;
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
}

/* 5. 결과창 박스 테두리에 네온 조명 효과 */
div[data-testid="stColorBlock"] {
    background: rgba(0, 0, 0, 0.2) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
}
</style>
"""
st.markdown(advanced_css, unsafe_allow_html=True)

# 2. 타이틀 네온 스타일링
st.markdown("<h1 style='text-align: center; color: #60A5FA; font-weight: 800; font-size: 2.2rem; text-shadow: 0 0 15px rgba(96,165,250,0.5);'>🧠 GLOBAL SDGs AI EVALUATION SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 1.05rem; margin-bottom: 2rem;'>지속가능발전목표(SDGs) 달성을 위한 AI 기반 아이디어 스코어링 및 고도화 플랫폼</p>", unsafe_allow_html=True)

st.divider()

# --- 🔒 보안 구현: Streamlit 비밀 금고(Secrets)에서 키 가져오기 ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("⚠️ Streamlit Secrets 설정에 'GEMINI_API_KEY'가 누락되었습니다! 대시보드 설정을 확인해 주세요.")
    st.stop()

# 3. 문제 분야 선택 (17개 SDGs 핵심 목표 반영)
issue_category = st.selectbox(
    "어떤 사회 문제에 관심이 있나요?",
    [
        "선택하세요", 
        "무빈곤 및 보건·복지 (Goal 1, 3) 🏥",
        "모두를 위한 양질의 교육 (Goal 4) 📚",
        "기후변화 대응 및 해양·육상 생태계 보전 (Goal 13, 14, 15) 🌍", 
        "불평등 완화 및 인권 존중 (Goal 10) 🤝", 
        "신재생 에너지 및 깨끗한 물 (Goal 6, 7) ⚡", 
        "기아 종식 및 지속가능한 농업 (Goal 2) 🌾", 
        "산업 혁신, 인프라 및 지속가능한 도시 (Goal 9, 11) 🏭"
    ]
)

if issue_category != "선택하세요":
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("💡 아이디어 제안")
    user_idea = st.text_input("우리가 실천할 수 있는 구체적인 방법을 적어주세요:", placeholder="예: 학교 급식 잔반을 이용한 퇴비화 및 지역 농가 기부")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("AI 심층 분석 시작하기", use_container_width=True):
        if user_idea.strip() == "":
            st.warning("내용을 입력해 주세요!")
        else:
            with st.spinner("🔄 AI 멘토가 문맥 분석 및 아이디어 고도화 방안을 생성 중입니다..."):
                try:
                    # AI 프롬프트
                    prompt = f"""
                    너는 SDGs(지속가능발전목표) 사회문제 해결 경진대회의 전문 심사위원 AI이자 전문 컨설턴트이다.
                    사용자가 '{issue_category}' 분야에 대해 다음과 같은 아이디어를 제안했다:
                    
                    [사용자 제안]: "{user_idea}"
                    
                    이 제안의 문맥을 분석하여 실현 가능성과 가치를 평가해라. 장난이거나 헛소리면 '부적절'로 판정해라.
                    반드시 아래의 양식으로만 답변해라. 다른 말은 절대로 하지 마라.
                    
                    [양식]
                    판정: (우수 / 보통 / 개선 필요 / 부적절 중 하나 선택)
                    점수: (0점에서 100점 사이의 숫자와 점 뒤에 '점'을 붙일 것. 예: 85점)
                    이유: (왜 그렇게 판정했는지 구체적이고 논리적인 설명)
                    개선안: (아이디어를 더 발전시키기 위한 구체적인 AI 개선 제안 3가지를 한 문장씩 적을 것. 예: 1. ~ / 2. ~ / 3. ~)
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    
                    ai_result = response.text
                    st.divider()
                    
                    # AI의 답변 쪼개서 정리하기
                    lines = ai_result.strip().split('\n')
                    status = "보통"
                    score_val = "50점"
                    reason_val = ""
                    suggestions = []
                    
                    for line in lines:
                        if "판정:" in line:
                            status = line.replace("판정:", "").strip()
                        elif "점수:" in line:
                            score_val = line.replace("점수:", "").strip()
                        elif "이유:" in line:
                            reason_val = line.replace("이유:", "").strip()
                        elif line.strip().startswith(("1.", "2.", "3.")) or "개선안:" in line:
                            if "개선안:" not in line:
                                suggestions.append(line.strip())
                    
                    try:
                        score_num = int(score_val.replace("점", "").strip())
                    except:
                        score_num = 50
                    
                    # --- 🎨 결과창 디자인 ---
                    with st.container(border=True):
                        st.markdown("<h3 style='color: #60A5FA;'>📊 AI 심사 심층 결과</h3>", unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if "우수" in status:
                                st.success(f"✨ **최종 판정: {status}**")
                                st.balloons() 
                            elif "보통" in status:
                                st.info(f"ℹ️ **최종 판정: {status}**")
                            elif "개선 필요" in status:
                                st.warning(f"⚠️ **최종 판정: {status}**")
                            else:
                                st.error(f"🚨 **최종 판정: {status}**")
                        
                        with col2:
                            delta_msg = "합격 (우수)" if "우수" in status or "보통" in status else "주의 (보완 필요)"
                            delta_color = "normal" if "우수" in status or "보통" in status else "inverse"
                            st.metric(label="아이디어 실현 가능성 점수", value=f"{score_num} / 100", delta=delta_msg, delta_color=delta_color)
                        
                        st.write("**스코어 진행도:**")
                        st.progress(score_num / 100)
                        
                        st.markdown(f"<div style='background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; margin-top: 1rem;'><strong>📝 종합 심사평:</strong><br>{reason_val}</div>", unsafe_allow_html=True)
                    
                    # 🚀 AI의 아이디어 고도화 추천 제안 출력
                    if suggestions and ("부적절" not in status):
                        st.write("")
                        with st.expander("🚀 아이디어를 업그레이드하기 위한 AI의 비밀 제안 (열기)", expanded=True):
                            for sug in suggestions:
                                st.markdown(f"<p style='color: #F3F4F6;'>{sug}</p>", unsafe_allow_html=True)
                                
                except Exception as e:
                    st.error(f"AI 연결 중 에러가 발생했습니다: {e}")
