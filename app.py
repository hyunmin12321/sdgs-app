import streamlit as st
from google import genai
from google.genai import types

# 1. 페이지 설정 (대회용 전문적인 타이틀)
st.set_page_config(page_title="AI 기반 SDGs 아이디어 평가 시스템", page_icon="🧠", layout="centered")

st.title("🧠 AI 기반 글로벌 SDGs 아이디어 스코어링 및 고도화 시스템")
st.write("구글 Gemini AI가 여러분의 아이디어를 심층 분석하고 발전적인 개선안을 제시합니다.")

st.divider()

# --- 🔒 4번 보안 구현: Streamlit 비밀 금고(Secrets)에서 키 가져오기 ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("⚠️ Streamlit Secrets 설정에 'GEMINI_API_KEY'가 누락되었거나 올바르지 않습니다! 대시보드 설정을 확인해 주세요.")
    st.stop()

# 2. 문제 분야 선택
issue_category = st.selectbox(
    "어떤 사회 문제에 관심이 있나요?",
    [
        "선택하세요", 
        "빈곤 퇴치 및 건강 🏥",
        "양질의 교육 제공 📚",
        "기후변화와 환경 오염 🌍", 
        "불평등 해소 🤝", 
        "깨끗한 에너지 ⚡", 
        "기아 종식 및 식량 안보 🌾", 
        "산업, 혁신 및 인프라 🏭"
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
                    
                    # '85점'에서 숫자 85만 쏙 빼와서 숫자로 변환
                    try:
                        score_num = int(score_val.replace("점", "").strip())
                    except:
                        score_num = 50
                    
                    # --- 🎨 2번 디자인 구현: 결과창 상자 및 게이지 바 ---
                    with st.container(border=True):
                        st.subheader("📊 AI 심사 심층 결과")
                        
                        # 화면을 반으로 쪼개서 깔끔하게 배치
                        col1, col2 = st.columns(2)
                        with col1:
                            if "우수" in status:
                                st.success(f"✨ **최종 판정: {status}**")
                                st.balloons() # 우수하면 풍선 날리기! 🎈
                            elif "보통" in status:
                                st.info(f"ℹ️ **최종 판정: {status}**")
                            elif "개선 필요" in status:
                                st.warning(f"⚠️ **최종 판정: {status}**")
                            else:
                                st.error(f"🚨 **최종 판정: {status}**")
                        
                        with col2:
                            # 4단계 판정에 따른 안내 문구 색상 세팅
                            delta_msg = "합격 (우수)" if "우수" in status or "보통" in status else "주의 (보단/부적절)"
                            delta_color = "normal" if "우수" in status or "보통" in status else "inverse"
                            st.metric(label="아이디어 실현 가능성 점수", value=f"{score_num} / 100", delta=delta_msg, delta_color=delta_color)
                        
                        # 📊 점수 게이지 바 (시각적 효과 극대화!)
                        st.write("**스코어 진행도:**")
                        st.progress(score_num / 100)
                        
                        st.markdown(f"**📝 종합 심사평:**\n{reason_val}")
                    
                    # 🚀 챗GPT 추천: AI의 아이디어 고도화 추천 제안 출력
                    if suggestions and ("부적절" not in status):
                        st.write("")
                        with st.expander("🚀 아이디어를 업그레이드하기 위한 AI의 비밀 제안 (열기)", expanded=True):
                            for sug in suggestions:
                                st.write(sug)
                                
                except Exception as e:
                    st.error(f"AI 연결 중 에러가 발생했습니다: {e}")
