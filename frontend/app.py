import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="Job Agent", layout="wide")
st.title("🤖 Job Agent")
st.caption("채용공고 분석 · 이력서 매칭 · 자소서 생성 자동화")

tab1, tab2, tab3 = st.tabs(["📋 공고 분석", "📊 이력서 매칭", "✍️ 자소서 생성"])

# ── 탭 1: 공고 분석 ──────────────────────────────
with tab1:
    st.subheader("채용공고 분석")
    job_url = st.text_input("채용공고 URL을 입력하세요")

    if st.button("분석 시작", key="analyze"):
        if not job_url:
            st.warning("URL을 입력해주세요")
        else:
            with st.spinner("공고 분석 중..."):
                res = requests.get(f"{API_URL}/analyze", params={"url": job_url})
                if res.status_code == 200:
                    data = res.json()["job_info"]
                    st.success("분석 완료")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("회사", data.get("company", "-"))
                        st.metric("직무", data.get("position", "-"))
                        st.metric("경력", data.get("experience", "-"))
                    with col2:
                        st.write("**필수 스킬**")
                        for skill in data.get("required_skills", []):
                            st.badge(skill)
                        st.write("**우대 스킬**")
                        for skill in data.get("preferred_skills", []):
                            st.badge(skill)
                    st.info(data.get("summary", ""))
                else:
                    st.error("분석 실패. URL을 확인해주세요.")

# ── 탭 2: 이력서 매칭 ──────────────────────────────
with tab2:
    st.subheader("이력서 매칭 분석")
    job_url2 = st.text_input("채용공고 URL", key="url2")
    resume_file2 = st.file_uploader("이력서 PDF 업로드", type=["pdf"], key="resume2")

    if st.button("매칭 분석", key="match"):
        if not job_url2 or not resume_file2:
            st.warning("URL과 이력서를 모두 입력해주세요")
        else:
            with st.spinner("매칭 분석 중..."):
                res = requests.post(
                    f"{API_URL}/match",
                    params={"job_url": job_url2},
                    files={"file": (resume_file2.name, resume_file2, "application/pdf")}
                )
                if res.status_code == 200:
                    data = res.json()
                    match = data["match_result"]
                    st.success("매칭 완료")
                    st.metric("매칭 점수", f"{match.get('score', 0)} / 100")
                    st.info(match.get("summary", ""))
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**✅ 보유 스킬**")
                        for skill in match.get("matched_skills", []):
                            st.badge(skill)
                    with col2:
                        st.write("**❌ 부족한 스킬**")
                        for skill in match.get("missing_skills", []):
                            st.badge(skill)
                else:
                    st.error("매칭 실패")

# ── 탭 3: 자소서 생성 ──────────────────────────────
with tab3:
    st.subheader("자소서 초안 생성")
    job_url3 = st.text_input("채용공고 URL", key="url3")
    resume_file3 = st.file_uploader("이력서 PDF 업로드", type=["pdf"], key="resume3")

    if st.button("자소서 생성", key="cover"):
        if not job_url3 or not resume_file3:
            st.warning("URL과 이력서를 모두 입력해주세요")
        else:
            with st.spinner("자소서 생성 중... (30초 정도 걸려요)"):
                res = requests.post(
                    f"{API_URL}/cover-letter",
                    params={"job_url": job_url3},
                    files={"file": (resume_file3.name, resume_file3, "application/pdf")}
                )
                if res.status_code == 200:
                    data = res.json()
                    cover = data["cover_letter"]
                    st.success("자소서 생성 완료")
                    st.subheader("지원동기")
                    st.write(cover.get("motivation", ""))
                    st.subheader("직무 관련 경험")
                    st.write(cover.get("experience", ""))
                    st.subheader("입사 후 포부")
                    st.write(cover.get("goal", ""))
                else:
                    st.error("자소서 생성 실패")