import json
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="서술형 자동 채점 시스템", page_icon="📝", layout="wide"
)

st.title("📝 서술형 문항 자동 채점 시스템")
st.caption(
    "조건 기반 의미 채점, 선택지별 모범답안 매칭 및 오개념 방지 로직 적용"
)

# ------------------------------------------------------------------------------
# 1. 문항 데이터 정의 (선택지별 모범답안 및 채점 기준 포함)
# ------------------------------------------------------------------------------
QUESTIONS = {
    "q1": {
        "title": "[문항 1] 문제 해결 방법 선택 및 당위성 서술",
        "score": 10,
        "type": "choice_essay",
        "choices": [
            "방법 A (정량적 분석)",
            "방법 B (정성적 인터뷰)",
            "방법 C (실험 검증)",
        ],
        "model_answers": {
            "방법 A (정량적 분석)": "수치화된 데이터를 바탕으로 객관적인 경향성을 파악하여 통계적 유의성을 확보할 수 있다.",
            "방법 B (정성적 인터뷰)": "사용자의 깊이 있는 맥락과 잠재된 요구사항(니즈)을 다각도로 포착할 수 있다.",
            "방법 C (실험 검증)": "변인을 통제한 상태에서 원인과 결과 간의 명확한 인과관계를 입증할 수 있다.",
        },
        "rubric": [
            "선택한 방법의 고유 특성/원리가 드러나는가?",
            "전문 용어가 없어도 방법의 의미가 올바르게 전달되었는가?",
            "다른 방법의 특성을 혼용하는 오개념이 없는가?",
            "최종 문제 해결 가능 여부에 대한 결론 방향이 명확한가?",
        ],
    },
    "q2": {
        "title": "[문항 2] 현상 원인 분석 및 결론 도출",
        "score": 10,
        "type": "essay",
        "choices": None,
        "model_answers": {
            "공통 모범답안": "원인 변인이 증가함에 따라 결과 상태가 둔화되며, 따라서 최종적으로 공정을 재조정해야 한다."
        },
        "rubric": [
            "원인과 결과의 메커니즘이 의미상 통하는가?",
            "결론의 방향(재조정 필요/불필요 등)이 명확히 명시되었는가?",
            "상반된 개념의 용어를 섞어 쓰는 오개념이 없는가?",
        ],
    },
}


# ------------------------------------------------------------------------------
# 2. 채점 시뮬레이션 함수 (규칙 기반 시뮬레이터)
# ------------------------------------------------------------------------------
def mock_auto_grade(q_id, user_ans, choice=None):
    """
    실제 환경에서는 OpenAI/Claude API를 호출하며,
    여기서는 주요 규칙 반영 여부를 시뮬레이션하여 검증합니다.
    """
    q_data = QUESTIONS[q_id]
    score = q_data["score"]
    reasons = []
    is_pass = True

    # [규칙 1] 결론 방향 확인
    conclusion_keywords = ["따라서", "결론", "해야 한다", "필요하다", "확보", "입증"]
    if not any(kw in user_ans for kw in conclusion_keywords):
        score -= 3
        reasons.append("❌ **결론 방향 미흡**: 요구된 결론이 명확하게 드러나지 않았습니다. (-3점)")
        is_pass = False

    # [규칙 2] 선택지별 특성 및 오개념 검증
    if choice:
        if "방법 A" in choice:
            if any(kw in user_ans for kw in ["인터뷰", "맥락", "깊이 있는"]):
                score -= 4
                reasons.append("❌ **오개념 감점**: 정량적 분석 선택 후 정성적 인터뷰의 특성을 서술함 (-4점)")
            elif not any(kw in user_ans for kw in ["수치", "데이터", "통계", "객관"]):
                # 용어가 없어도 의미 표현 인정 로직 예시
                if not any(kw in user_ans for kw in ["숫자", "모아서", "계산"]):
                    score -= 2
                    reasons.append("⚠️ **특성 미흡**: 선택한 방법(정량)의 핵심 원리/특성이 부족함 (-2점)")

        elif "방법 B" in choice:
            if any(kw in user_ans for kw in ["통계", "수치", "변인 통제"]):
                score -= 4
                reasons.append("❌ **오개념 감점**: 정성적 인터뷰 선택 후 다른 방법의 특성을 서술함 (-4점)")

    # [규칙 3] 용어 없이 의미 인정 예시
    if "개념 용어 없이 의미 전달" in user_ans:
        reasons.append("✅ **유연 채점 인정**: 특정 전문 용어는 없으나 핵심 의미가 전달되어 정답 처리됨")

    if score == q_data["score"]:
        reasons.append("✅ **완벽한 답안**: 모든 채점 기준 및 오개념 방지 요건을 충족함")

    return {
        "score": max(0, score),
        "max_score": q_data["score"],
        "reasons": reasons,
    }


# ------------------------------------------------------------------------------
# 3. UI 레이아웃
# ------------------------------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 문항 및 답안 제출")

    selected_q_key = st.selectbox(
        "채점할 문항을 선택하세요",
        options=list(QUESTIONS.keys()),
        format_func=lambda x: QUESTIONS[x]["title"],
    )

    q = QUESTIONS[selected_q_key]

    st.markdown(f"**배점:** {q['score']}점")

    # 선택지가 있는 문항 처리
    selected_choice = None
    if q["type"] == "choice_essay":
        selected_choice = st.radio("적용할 방법/선택지를 선택하세요:", q["choices"])

    # 답안 입력
    user_input = st.text_area(
        "학생 답안 입력",
        height=180,
        placeholder="채점 기준 테스트용 답안을 입력하세요...",
    )

    submit_btn = st.button("🚀 자동 채점 실행", type="primary")

with col2:
    st.subheader("💡 채점 기준 및 모범 답안")

    # 모범 답안 출력
    with st.expander("📌 선택지별 모범 답안 보기", expanded=True):
        for c_name, m_ans in q["model_answers"].items():
            st.markdown(f"**[{c_name}]**")
            st.info(m_ans)

    # 채점 루브릭 출력
    with st.expander("🔍 주요 채점 반영 규칙", expanded=True):
        for r in q["rubric"]:
            st.write(f"- {r}")

    # 채점 결과 출력 영역
    st.markdown("---")
    st.subheader("📊 채점 결과")

    if submit_btn:
        if not user_input.strip():
            st.warning("답안을 입력해주세요.")
        else:
            result = mock_auto_grade(selected_q_key, user_input, selected_choice)

            # 점수 표시
            score_ratio = result["score"] / result["max_score"]
            if score_ratio == 1.0:
                st.success(f"### 최종 점수: {result['score']} / {result['max_score']} 점 (통과)")
            elif score_ratio >= 0.6:
                st.warning(f"### 최종 점수: {result['score']} / {result['max_score']} 점 (부분 점수)")
            else:
                st.error(f"### 최종 점수: {result['score']} / {result['max_score']} 점 (재검토/미통과)")

            # 채점 피드백 상세
            st.markdown("**[상세 피드백]**")
            for reason in result["reasons"]:
                st.write(reason)