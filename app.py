import streamlit as st
from google import genai
from google.genai import types

# 1. 페이지 설정 (대회용 전문적인 타이틀)
st.set_page_config(page_title="AI 기반 SDGs 아이디어 평가 시스템", page_icon="🧠", layout="centered")

# --- 🎨 4번 구현: SDGs 글로벌 지구본 배경 디자인 (CSS 마법) ---
# 전 세계 SDGs를 상징하는 원형 그래픽 배경을 사이트 전체에 깔아줍니다.
background_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1920"); /* 부드러운 글로벌 추상 배경 */
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
/* 글자가 잘 보이도록 중앙 컨테이너에 살짝 투명한 유리창 효과 주기 */
.block-container {
    background: rgba(255, 255, 255, 0.92);
    padding: 3rem;
    border-radius: 20px;
    box-shadow: 0px 8px 32px rgba(0, 0, 0, 0.1);
    margin-top: 2rem;
}
</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

# 2. 상단 타이틀 및 로고 연출
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🧠 AI 기반 글로벌 SDGs 아이디어 스코어링 시스템</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4B5563;'>구글 Gemini 2.5 AI가 17대 지속가능발전목표(SDGs)를 기반으로 아이디어를 고도화합니다.</p>", unsafe_allow_html=True)

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
    st.subheader("💡 아이디어 제안")
    user_idea = st.text_input("우리가 실천할 수 있는 구체적인 방법을 적어주세요:", placeholder="예: 학교 급식 잔반을 이용한 퇴비화 및 지역 농가 기부")
    
    if st.button("AI 심층 분석 시작하기", use_container_width=True):
        if user_idea.strip() == "":
            st.warning("내용을 입력해 주세요!")
        else:
            with st.spinner("🔄 AI 멘토가 문맥 분석 및 아이디어 고도화 방안을 생성 중입니다..."):
                try:
                    # AI에게 줄 특수 명령어 (프롬프트 튜닝)
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
                    
                    # Gemini AI에게 요청 보내기
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
                    
                    # --- 🎨 2번 디자인 구현: 결과창 상자 및 게이지 바 ---
                    with st.container(border=True):
                        st.subheader("📊 AI 심사 심층 결과")
                        
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
                        
                        # 📊 점수 게이지 바 효과
                        st.write("**스코어 진행도:**")
                        st.progress(score_num / 100)
                        
                        st.markdown(f"**📝 종합 심사평:**\n{reason_val}")
                    
                    # 🚀 AI의 아이디어 고도화 추천 제안 출력
                    if suggestions and ("부적절" not in status):
                        st.write("")
                        with st.expander("🚀 아이디어를 업그레이드하기 위한 AI의 비밀 제안 (열기)", expanded=True):
                            for sug in suggestions:
                                st.write(sug)
                                
                except Exception as e:
                    st.error(f"AI 연결 중 에러가 발생했습니다: {e}")
