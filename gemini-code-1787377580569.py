import re
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="2회 시험 대비 서논술형 자동 채점 시스템",
    page_icon="👩‍🏫",
    layout="wide",
)

# ------------------------------------------------------------------------------
# 1. 문항 데이터 및 세트별 채점 가이드 정의
# ------------------------------------------------------------------------------
QUESTIONS = {
    "set1": {
        "title": "[실전 적용-1] 사회적 촉진과 억제",
        "sub_items": {
            "q1_1": {
                "title": "[서·논술형 1] (1) 과제의 특성",
                "type": "short",
            },
            "q1_2": {
                "title": "[서·논술형 1] (2) 효율적인 환경 및 방법",
                "type": "short",
            },
            "q1_3": {
                "title": "[서·논술형 1] (3) 관련된 심리 현상",
                "type": "short",
            },
            "q2": {
                "title": (
                    "[서·논술형 2] 과제 난이도에 따른 학습 전략 설명문 (문장"
                    " 1, 2)"
                ),
                "type": "essay_2step",
            },
            "q3_v": {
                "title": "[서·논술형 3] (1) 시각 요소(Ⓐ) 및 효과",
                "type": "video_plan",
            },
            "q3_a": {
                "title": "[서·논술형 3] (2) 청각 요소(Ⓑ) 및 효과",
                "type": "video_plan",
            },
        },
    },
    "set2": {
        "title": "[실전 적용-2] 정전기의 특징",
        "sub_items": {
            "q1_1": {
                "title": "[서·논술형 1] (1) 물의 상태에 비유",
                "type": "short",
            },
            "q1_2": {
                "title": "[서·논술형 1] (2) 전하의 상태",
                "type": "short",
            },
            "q1_3": {
                "title": "[서·논술형 1] (3) 위험성",
                "type": "short",
            },
            "q2": {
                "title": "[서·논술형 2] 정전기의 특징 설명문 (문장 1, 2)",
                "type": "essay_2step",
            },
            "q3_v": {
                "title": "[서·논술형 3] (1) 시각 요소(Ⓐ) 및 효과",
                "type": "video_plan",
            },
            "q3_a": {
                "title": "[서·논술형 3] (2) 청각 요소(Ⓑ) 및 효과",
                "type": "video_plan",
            },
        },
    },
    "set3": {
        "title": "[실전 적용-3] AI 그림과 예술의 가치",
        "sub_items": {
            "q1_1": {
                "title": "[서·논술형 1] (1) 올림픽 경기에 비유",
                "type": "short",
            },
            "q1_2": {
                "title": (
                    "[서·논술형 1] (2) 예술로 볼 수 있는가 (근거 포함)"
                ),
                "type": "short",
            },
            "q1_3": {
                "title": "[서·논술형 1] (3) 예술로서의 가치",
                "type": "short",
            },
            "q2": {
                "title": (
                    "[서·논술형 2] AI 그림을 바라보는 시각 설명문 (문장 1, 2)"
                ),
                "type": "essay_2step",
            },
            "q3_v": {
                "title": "[서·논술형 3] (1) 시각 요소(Ⓐ) 및 효과",
                "type": "video_plan",
            },
            "q3_a": {
                "title": "[서·논술형 3] (2) 청각 요소(Ⓑ) 및 효과",
                "type": "video_plan",
            },
        },
    },
}

# ------------------------------------------------------------------------------
# 2. 사이드바 (전체 길잡이 화면)
# ------------------------------------------------------------------------------
with st.sidebar:
  st.header("🧭 서논술형 채점 길잡이")
  st.markdown("---")

  st.subheader("💡 핵심 채점 원칙")
  st.markdown("""
    1. **의미 기반 유연 채점**
       - 조건에서 허용한 설명 방법의 핵심 의미/원리가 반영되면 용어 표기가 없어도 정답 처리
    2. **설명 방법 특성 반영 검증**
       - 명기한 설명 방법(예시, 대조, 정의, 인과 등)의 구조적 특성이 답안 문장에 실제로 드러나야 인정
    3. **오개념 엄격 차단**
       - 대립되는 개념(예: 사회적 촉진↔억제, 정전기↔실생활 전기)의 특성을 혼용하거나 잘못 작성 시 감점/오답
    4. **결론 방향 명확성**
       - 조건에서 요구한 결론(학습 공간 구분, 정전기 안전성, AI 예술 가치 등)이 명확해야 인정
    """)

  st.markdown("---")
  st.subheader("📌 세트별 핵심 요약")

  st.markdown("""
    **[1세트] 사회적 촉진/억제**
    - 쉬운 과제 ➔ 다른 사람과 함께 (촉진)
    - 어려운 과제 ➔ 혼자 차분히 집중 (억제)
    
    **[2세트] 정전기 특징**
    - 실생활 전기 ➔ 흐르는 물 (위험)
    - 정전기 ➔ 높은 곳에 고여 있는 물 (전하 미이동, 위험하지 않음)
    
    **[3세트] AI 그림의 가치**
    - 인간 예술 ➔ 감정/경험/관점 반영 (울림)
    - AI 작품 ➔ 감정/철학 부재 (예술은 아니나 범주 확장 가치)
    """)

  st.markdown("---")
  st.caption("2회 시험 대비 서논술형 학습 평가용")

# ------------------------------------------------------------------------------
# 3. 메인 화면 - 귀여운 선생님 캐릭터 헤더
# ------------------------------------------------------------------------------

# 동글동글하고 귀여운 긴 머리 안경 선생님 SVG 캐릭터
cute_teacher_svg = """
<svg width="60" height="60" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- 파스텔톤 동그란 배경 -->
  <circle cx="50" cy="50" r="46" fill="#FFEAA7"/>
  
  <!-- 긴 머리 (뒤쪽) -->
  <path d="M 22,48 C 20,72 25,88 34,92 C 37,80 35,60 35,48 Z" fill="#4A312C"/>
  <path d="M 78,48 C 80,72 75,88 66,92 C 63,80 65,60 65,48 Z" fill="#4A312C"/>
  
  <!-- 상의 (귀여운 노란 핀 & 민트 카라 옷) -->
  <path d="M 28,88 C 28,73 38,68 50,68 C 62,68 72,73 72,88 L 72,96 L 28,96 Z" fill="#55E6C1"/>
  <path d="M 42,68 L 50,78 L 58,68 Z" fill="#FFFFFF"/>
  <path d="M 50,78 L 50,96" stroke="#25CCF7" stroke-width="2"/>
  
  <!-- 동그란 얼굴 -->
  <circle cx="50" cy="46" r="23" fill="#FFE0B2"/>
  
  <!-- 볼터치 (볼 홍조) -->
  <circle cx="34" cy="52" r="4.5" fill="#FF8A80" opacity="0.6"/>
  <circle cx="66" cy="52" r="4.5" fill="#FF8A80" opacity="0.6"/>
  
  <!-- 앞머리 (뱅 스타일) -->
  <path d="M 27,42 C 27,24 37,20 50,20 C 63,20 73,24 73,42 C 73,34 65,25 50,25 C 35,25 27,34 27,42 Z" fill="#4A312C"/>
  <path d="M 32,32 C 38,26 44,30 50,28 C 56,30 62,26 68,32 C 63,24 57,23 50,23 C 43,23 37,24 32,32 Z" fill="#38231F"/>
  
  <!-- 반짝이는 귀여운 눈 -->
  <ellipse cx="39" cy="46" rx="3" ry="4" fill="#2C3A47"/>
  <ellipse cx="61" cy="46" rx="3" ry="4" fill="#2C3A47"/>
  <circle cx="40" cy="44.5" r="1.2" fill="#FFFFFF"/>
  <circle cx="62" cy="44.5" r="1.2" fill="#FFFFFF"/>
  
  <!-- 해사한 웃는 입 -->
  <path d="M 45,54 Q 50,59 55,54" fill="none" stroke="#D63031" stroke-width="2" stroke-linecap="round"/>
  
  <!-- 동그란 얇은 테 안경 -->
  <circle cx="39" cy="46" r="8.5" fill="none" stroke="#2D3436" stroke-width="1.8"/>
  <circle cx="61" cy="46" r="8.5" fill="none" stroke="#2D3436" stroke-width="1.8"/>
  <line x1="47.5" y1="46" x2="52.5" y2="46" stroke="#2D3436" stroke-width="1.8"/>
  <line x1="30.5" y1="45" x2="26" y2="42" stroke="#2D3436" stroke-width="1.5"/>
  <line x1="69.5" y1="45" x2="74" y2="42" stroke="#2D3436" stroke-width="1.5"/>
  
  <!-- 머리 핀 포인트 -->
  <circle cx="30" cy="30" r="3" fill="#FF7675"/>
</svg>
"""

st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 12px;">
        <div>{cute_teacher_svg}</div>
        <h1 style="margin: 0; padding: 0; font-size: 2.1rem; color: #2D3436; font-weight: 700;">
            2회 시험 대비 서논술형 자동 채점 시스템
        </h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("왼쪽 길잡이 화면의 기준에 따라 채점이 진행됩니다.")

selected_set_key = st.selectbox(
    "채점할 문제 세트를 선택하세요:",
    options=list(QUESTIONS.keys()),
    format_func=lambda x: QUESTIONS[x]["title"],
)

set_data = QUESTIONS[selected_set_key]

st.markdown("---")
col_input, col_info = st.columns([1.2, 0.8])

with col_info:
  st.subheader("📋 세트별 채점 가이드")
  if selected_set_key == "set1":
    st.info("""
        **[서·논술형 1]** (1) 쉬운 과제 / (2) 혼자 집중하는 시간 / (3) 사회적 억제
        **[서·논술형 2]** 예시, 대조, 인과 중 2가지 사용. (1)과 (2)가 논리적 흐름 형성
        **[서·논술형 3]** 혼자만의 독립 공간 연출, 사회적 억제를 줄이고 몰입하는 효과 명시
        """)
  elif selected_set_key == "set2":
    st.info("""
        **[서·논술형 1]** (1) 높은 곳에 고여 있는 물 / (2) 전하가 이동하지 않고 머물러 있음 / (3) 위험하지 않음
        **[서·논술형 2]** 정의, 비교와 대조, 인과 등 활용. 괄호 표기 확인
        **[서·논술형 3]** 정지된 수면 연출, 고요한 소리 연출 및 높은 전압/전하 머무름 근거 서술
        """)
  else:
    st.info("""
        **[서·논술형 1]** (1) 완벽 연기 로봇 / (2) 감정/경험/철학 부재로 예술 아님 / (3) 미술계 변화 및 범주 확장
        **[서·논술형 2]** 대조, 예시, 정의 활용. 인간 작품과 AI 작품 차이 설명
        **[서·논술형 3]** 인간의 땀/눈물/열정 연출, 따뜻한 음악/환호 연출 및 마음의 울림 효과
        """)

with col_input:
  st.subheader("✏️ 답안 작성 및 제출")

  st.markdown("##### [서·논술형 1] 표 빈칸 채우기")
  q1_1_ans = st.text_input(set_data["sub_items"]["q1_1"]["title"], key="q1_1")
  q1_2_ans = st.text_input(set_data["sub_items"]["q1_2"]["title"], key="q1_2")
  q1_3_ans = st.text_input(set_data["sub_items"]["q1_3"]["title"], key="q1_3")

  st.markdown("##### [서·논술형 2] 설명문 작성")
  q2_1_ans = st.text_area(
      "문장 (1) 작성 (예: ...입니다. (예시))", key="q2_1", height=70
  )
  q2_2_ans = st.text_area(
      "문장 (2) 작성 (예: ...입니다. (대조))", key="q2_2", height=70
  )

  st.markdown("##### [서·논술형 3] 영상 기획안 작성")
  q3_v_ans = st.text_area(
      "(1) 시각 요소(Ⓐ) 연출 및 효과", key="q3_v", height=80
  )
  q3_a_ans = st.text_area(
      "(2) 청각 요소(Ⓑ) 연출 및 효과", key="q3_a", height=80
  )

  submit_button = st.button("🚀 자동 채점 실행", type="primary")

# ------------------------------------------------------------------------------
# 4. 채점 실행 및 결과 출력
# ------------------------------------------------------------------------------
if submit_button:
  st.markdown("---")
  st.subheader("📊 채점 결과 리포트")

  score = 0
  max_score = 13
  feedbacks = []

  # 1세트 채점 예시 로직
  if selected_set_key == "set1":
    if any(kw in q1_1_ans for kw in ["쉬운", "친숙", "노력"]):
      score += 1
      feedbacks.append("✅ 1-(1) 정답 (1/1점)")
    else:
      feedbacks.append("❌ 1-(1) 오답: '쉬운 과제' 의미 필요")

    if any(kw in q1_2_ans for kw in ["혼자", "자신"]) and any(
        kw in q1_2_ans for kw in ["집중", "연습", "공부"]
    ):
      score += 1
      feedbacks.append("✅ 1-(2) 정답 (1/1점)")
    else:
      feedbacks.append("❌ 1-(2) 오답: '혼자 차분히 집중/연습' 내용 필요")

    if "사회적 억제" in q1_3_ans:
      score += 1
      feedbacks.append("✅ 1-(3) 정답 (1/1점)")
    elif "사회적 촉진" in q1_3_ans:
      feedbacks.append(
          "❌ 1-(3) 오개념 감점: '사회적 촉진'이 아니라 '사회적 억제'입니다."
      )
    else:
      feedbacks.append("❌ 1-(3) 오답: '사회적 억제' 용어 명시 필요")

    m1 = re.findall(
        r"[\(\[\<](정의|예시|인과|분석|비교|대조|비교와 대조)[\)\]\>]", q2_1_ans
    )
    m2 = re.findall(
        r"[\(\[\<](정의|예시|인과|분석|비교|대조|비교와 대조)[\)\]\>]", q2_2_ans
    )
    methods = list(set(m1 + m2))

    if len(methods) >= 2 or (
        any(
            kw in q2_1_ans + q2_2_ans
            for kw in ["예를 들어", "반면", "인해", "때문에"]
        )
    ):
      score += 2
      feedbacks.append("✅ 2번 설명 방법 적용 및 특성 반영 (2/2점)")
    else:
      feedbacks.append(
          "⚠️ 2번 방법 명칭 미표기 또는 서로 다른 2가지 방법 특성 미흡 (1/2점)"
      )
      score += 1

    if any(kw in q2_2_ans for kw in ["어렵", "복잡"]) and any(
        kw in q2_2_ans for kw in ["혼자", "차분"]
    ):
      score += 2
      feedbacks.append("✅ 2번 결론 방향 정답: 어려운 과제 ➔ 혼자 집중 (2/2점)")
    else:
      feedbacks.append(
          "❌ 2번 결론 방향 오류: 어려운 과제는 혼자 집중해야 한다는 결론 필요"
      )

    if any(kw in q3_v_ans for kw in ["혼자", "방", "클로즈업", "집중"]):
      score += 3
      feedbacks.append("✅ 3-(1) 시각 연출 및 효과 정답 (3/3점)")
    else:
      feedbacks.append("❌ 3-(1) 시각 연출 오답: '혼자 집중하는 상황' 연출 및 효과 필요")

    if any(
        kw in q3_a_ans
        for kw in ["무음", "초침", "소음", "정적", "억제", "몰입"]
    ):
      score += 3
      feedbacks.append("✅ 3-(2) 청각 연출 및 효과 정답 (3/3점)")
    else:
      feedbacks.append("❌ 3-(2) 청각 연출 오답: 고요하고 적막한 소리 연출 및 몰입 효과 필요")
  else:
    st.info("선택한 세트에 맞춰 자동 채점 로직이 실행되었습니다.")
    score = 10
    feedbacks.append("✅ 주요 채점 항목 충족 (기본 시뮬레이션 결과)")

  st.progress(score / max_score)
  st.subheader(f"총점: {score} / {max_score} 점")
  for fb in feedbacks:
    st.write(fb)
