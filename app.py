import streamlit as st
from google import genai
from google.genai import types

# 1. 페이지 설정 (대회용으로 전문적인 제목 변경!)
st.set_page_config(page_title="AI 기반 SDGs 아이디어 평가 시스템", page_icon="🧠", layout="centered")

st.title("🧠 AI 기반 글로벌 SDGs 아이디어 스코어링 및 고도화 시스템")
st.write("구글 Gemini AI가 여러분의 아이디어를 심층 분석하고 발전적인 개선안을 제시합니다.")

st.divider()

# --- AI 연결 설정 ---
API_KEY = "AQ.Ab8RN6LNNyq5tJMmcio-srdjboxhGG0Nony3qu5XPOFJsP8OuQ" 

if API_KEY == "YOUR_API_KEY_HERE":
    st.error("⚠️ 코드를 열어서 'YOUR_API_KEY_HERE' 부분에 실제 구글 API Key를 입력해 주세요!")
else:
    client = genai.Client(api_key=API_KEY)

    # 2. 문제 분야 선택 (쉼표 오타 수정 및 분야 다양화!)
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
        user_idea = st.text_input("우리가 실천할 수 있는 구체적인 방법을 적어주세요:")
        
        if st.button("AI 심층 분석 시작하기"):
            if user_idea.strip() == "":
                st.warning("내용을 입력해 주세요!")
            else:
                with st.spinner("🔄 AI 멘토가 문맥 분석 및 아이디어 고도화 방안을 생성 중입니다..."):
                    try:
                        # 챗GPT 피드백 반영: 4단계 판정 및 '개선 제안' 요구 추가!
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
                        
                        # AI의 답변을 쪼개서 변수에 담기
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
                        
                        # 화면에 결과 출력 (4단계 판정 연동)
                        if "우수" in status or "보통" in status:
                            if "우수" in status:
                                st.balloons() # 우수 등급은 축하 풍선! 🎈
                                st.success(f"✨ **AI 판독 결과: {status}**")
                            else:
                                st.info(f"ℹ️ **AI 판독 결과: {status}**")
                                
                            st.write(f"**심사평:** {reason_val}")
                            st.metric(label="아이디어 실현 가능성 점수", value=score_val, delta=f"등급: {status}")
                            
                            # 챗GPT 강추 기능: AI 개선 제안 화면 표시
                            if suggestions:
                                st.subheader("🚀 AI의 아이디어 고도화 추천 제안")
                                for sug in suggestions:
                                    st.write(sug)
                        else:
                            st.error(f"🚨 **AI 판독 결과: {status}**")
                            st.write(f"**심사평:** {reason_val}")
                            st.metric(label="아이디어 실현 가능성 점수", value=score_val, delta=f"주의 ({status})", delta_color="inverse")
                            
                    except Exception as e:
                        st.error(f"AI 연결 중 에러가 발생했습니다: {e}")
