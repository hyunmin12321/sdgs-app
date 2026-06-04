import streamlit as st
from google import genai
from google.genai import types

# 1. 페이지 설정
st.set_page_config(page_title="진짜 AI SDGs 판독기", page_icon="🧠", layout="centered")

st.title("🧠 진짜 AI 사회문제 해결 아이디어 판독기")
st.write("구글 Gemini AI가 여러분의 아이디어 문맥을 완벽하게 분석합니다!")

st.divider()

# --- AI 연결 설정 ---
# 주의: 아래 따옴표 안에 아까 발급받은 Google API Key를 넣어줘!
API_KEY = "AQ.Ab8RN6LNNyq5tJMmcio-srdjboxhGG0Nony3qu5XPOFJsP8OuQ" 

if API_KEY == "YOUR_API_KEY_HERE":
    st.error("⚠️ 코드를 열어서 'YOUR_API_KEY_HERE' 부분에 실제 구글 API Key를 입력해 주세요!")
else:
    client = genai.Client(api_key=API_KEY)

    # 2. 문제 분야 선택
    issue_category = st.selectbox(
        "어떤 사회 문제에 관심이 있나요?",
        ["선택하세요", "기후변화와 환경 오염 🌍", "불평등 해소 🤝", "깨끗한 에너지 ⚡"]
    )

    if issue_category != "선택하세요":
        st.subheader("💡 아이디어 제안")
        user_idea = st.text_input("우리가 실천할 수 있는 구체적인 방법을 적어주세요:")
        
        if st.button("AI 심층 분석 시작하기"):
            if user_idea.strip() == "":
                st.warning("내용을 입력해 주세요!")
            else:
                with st.spinner("🔄 진짜 AI가 문맥과 의미를 심층 분석하고 있습니다..."):
                    try:
                        # AI에게 줄 특수 명령어 (프롬프트 엔지니어링)
                        prompt = f"""
                        너는 SDGs(지속가능발전목표) 사회문제 해결 경진대회의 전문 심사위원 AI이다.
                        사용자가 '{issue_category}' 분야에 대해 다음과 같은 아이디어를 제안했다:
                        
                        [사용자 제안]: "{user_idea}"
                        
                        이 제안이 장난이거나 문맥상 불가능한 헛소리인지, 아니면 진짜 실천 가능한 좋은 제안인지 문맥을 파악해서 분석해라.
                        반드시 아래의 양식으로만 답변해라. 다른 말은 하지 마라.
                        
                        [양식]
                        판정: (좋은 제안 / 부적절한 제안 중 하나 선택)
                        점수: (0점에서 100점 사이의 숫자와 점 뒤에 '점'을 붙일 것. 예: 85점)
                        이유: (왜 그렇게 판정했는지 친절하고 논리적인 한글 설명)
                        """
                        
                        # Gemini AI에게 요청 보내기
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt,
                        )
                        
                        ai_result = response.text
                        st.divider()
                        
                        # AI의 답변을 보기 좋게 쪼개서 화면에 출력하기
                        lines = ai_result.strip().split('\n')
                        status = "보통"
                        score_val = "50점"
                        reason_val = ""
                        
                        for line in lines:
                            if "판정:" in line:
                                status = line.replace("판정:", "").strip()
                            elif "점수:" in line:
                                score_val = line.replace("점수:", "").strip()
                            elif "이유:" in line:
                                reason_val = line.replace("이유:", "").strip()
                        
                        # 화면에 결과 뿌려주기
                        if "좋은" in status:
                            st.balloons() # 축하 풍선 🎈
                            st.success(f"✨ **AI 판독 결과: {status}**")
                            st.write(reason_val)
                            st.metric(label="아이디어 실현 가능성 점수", value=score_val, delta="합격 (우수)")
                        else:
                            st.error(f"🚨 **AI 판독 결과: {status}**")
                            st.write(reason_val)
                            st.metric(label="아이디어 실현 가능성 점수", value=score_val, delta="-경고 (장난/불가능)", delta_color="inverse")
                            
                    except Exception as e:
                        st.error(f"AI 연결 중 에러가 발생했습니다: {e}")