import html
from datetime import datetime

import streamlit as st

from generator import generate_interview


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Placement Prep Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# DESIGN SYSTEM
# Ink #16213E | Teal #0E8388 | Mist #F3F6FA | Amber #F4A93B | White
# Fonts: Sora (headings) + Inter (body)
# --------------------------------------------------

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@500;600;700&display=swap');

:root {
    --ink: #16213E;
    --ink-soft: #4A5578;
    --teal: #0E8388;
    --teal-light: #E3F4F4;
    --mist: #F3F6FA;
    --amber: #F4A93B;
    --amber-light: #FFF6E5;
    --line: #E2E8F0;
    --white: #FFFFFF;
}

html, body, [class*="css"], .stMarkdown, p, li, label {
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}

h1, h2, h3, h4 {
    font-family: 'Sora', sans-serif !important;
    color: var(--ink) !important;
    letter-spacing: -0.01em;
}

.stApp { background: var(--mist); }

/* Hide default Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1100px; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: var(--white);
    border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

.side-brand {
    display: flex; align-items: center; gap: 12px; margin-bottom: 6px;
}
.side-logo {
    width: 42px; height: 42px; border-radius: 12px;
    background: linear-gradient(135deg, var(--teal), var(--ink));
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
}
.side-title { font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.05rem; color: var(--ink); line-height: 1.2; }
.side-sub { color: var(--ink-soft); font-size: 0.85rem; margin: 0 0 1.2rem 0; }

div[data-baseweb="select"] > div {
    border-radius: 10px; border-color: var(--line); background: var(--white);
}

/* Primary button */
.stButton > button[kind="primary"], .stDownloadButton > button {
    background: linear-gradient(135deg, var(--teal), #0B6B70);
    color: #fff; border: none; border-radius: 12px;
    font-family: 'Sora', sans-serif; font-weight: 600;
    padding: 0.75rem 1rem;
    box-shadow: 0 6px 16px rgba(14, 131, 136, 0.28);
    transition: transform .15s ease, box-shadow .15s ease;
}
.stButton > button[kind="primary"]:hover, .stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 22px rgba(14, 131, 136, 0.35);
    color: #fff; border: none;
}

/* ---------- Hero ---------- */
.hero {
    background: linear-gradient(120deg, var(--ink) 0%, #243B6B 60%, #0E8388 130%);
    border-radius: 24px;
    padding: 44px 48px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: ""; position: absolute; right: -60px; top: -60px;
    width: 260px; height: 260px; border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.hero-greeting { color: #BFE9EA; font-size: 1rem; margin: 0 0 10px 0; }
.hero h1 {
    color: #fff !important; font-size: 2.4rem; line-height: 1.2;
    margin: 0 0 14px 0; max-width: 640px;
}
.hero p { color: #D5DCF0; font-size: 1.05rem; line-height: 1.6; max-width: 600px; margin: 0; }

/* ---------- Feature tiles (welcome) ---------- */
.tile {
    background: var(--white); border: 1px solid var(--line);
    border-radius: 16px; padding: 22px; height: 100%;
}
.tile .ico { font-size: 1.6rem; margin-bottom: 8px; }
.tile h4 { margin: 0 0 6px 0; font-size: 1rem; }
.tile p { margin: 0; color: var(--ink-soft); font-size: 0.92rem; line-height: 1.55; }

/* ---------- Result header ---------- */
.result-head {
    background: var(--white); border: 1px solid var(--line);
    border-radius: 18px; padding: 22px 26px; margin-bottom: 18px;
}
.result-head h2 { margin: 0 0 4px 0; font-size: 1.4rem; }
.result-head .meta { color: var(--ink-soft); font-size: 0.95rem; }

/* ---------- Badges ---------- */
.badge {
    display: inline-block; padding: 4px 12px; border-radius: 999px;
    font-size: 0.8rem; font-weight: 500; margin-right: 8px;
}
.badge-type { background: var(--teal-light); color: #0A5F63; }
.badge-easy { background: #E6F6EC; color: #1C7A3F; }
.badge-medium { background: var(--amber-light); color: #9A6410; }
.badge-hard { background: #FDEAEA; color: #A32D2D; }

/* ---------- Expanders (question cards) ---------- */
div[data-testid="stExpander"] {
    background: var(--white);
    border: 1px solid var(--line) !important;
    border-radius: 16px !important;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(22, 33, 62, 0.04);
}
div[data-testid="stExpander"] summary { padding: 14px 18px; }
div[data-testid="stExpander"] summary p {
    font-family: 'Sora', sans-serif; font-weight: 600; font-size: 1.02rem;
}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] { font-family: 'Inter', sans-serif; font-weight: 500; }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--teal); }
div[data-baseweb="tab-highlight"] { background-color: var(--teal) !important; }

/* ---------- Callouts ---------- */
.callout {
    border-radius: 14px; padding: 16px 18px; line-height: 1.6; font-size: 0.97rem;
}
.callout-teal { background: var(--teal-light); border-left: 4px solid var(--teal); }
.callout-amber { background: var(--amber-light); border-left: 4px solid var(--amber); }
.callout-title { font-family: 'Sora', sans-serif; font-weight: 600; margin-bottom: 6px; }

/* ---------- Keyword chips ---------- */
.chip {
    display: inline-block; background: var(--mist); border: 1px solid var(--line);
    color: var(--ink); padding: 5px 12px; border-radius: 8px;
    font-size: 0.85rem; margin: 0 8px 8px 0;
}

/* ---------- Progress ---------- */
.stProgress > div > div > div > div { background-color: var(--teal); }

/* ---------- Mobile ---------- */
@media (max-width: 700px) {
    .hero { padding: 28px 24px; }
    .hero h1 { font-size: 1.7rem; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def greeting() -> str:
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning ☀️"
    if hour < 17:
        return "Good afternoon 👋"
    return "Good evening 🌙"


def esc(text) -> str:
    return html.escape(str(text))


def difficulty_badge(level: str) -> str:
    css = {
        "easy": "badge-easy",
        "medium": "badge-medium",
        "hard": "badge-hard",
    }.get(str(level).strip().lower(), "badge-medium")
    return f'<span class="badge {css}">{esc(level)}</span>'


def build_download_text(result) -> str:
    lines = [f"{result.job_role} | {result.experience_level}", "=" * 60, ""]
    for i, q in enumerate(result.questions, start=1):
        lines += [
            f"Q{i}. {q.question}",
            f"Type: {q.question_type} | Difficulty: {q.difficulty}",
            "",
            "Model answer:",
            str(q.model_answer),
            "",
            "In simple words:",
            str(q.explanation),
            "",
            "Practical example:",
            str(q.practical_example),
            "",
            "Keywords: " + ", ".join(q.keywords),
            "",
            f"Follow-up: {q.follow_up}",
            "",
            "-" * 60,
            "",
        ]
    return "\n".join(lines)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div class="side-brand">
            <div class="side-logo">🎯</div>
            <div class="side-title">Placement<br>Prep Coach</div>
        </div>
        <p class="side-sub">Tell us about the role you're aiming for. We'll build your practice set.</p>
        """,
        unsafe_allow_html=True,
    )

    job_role = st.selectbox(
        "Which role are you preparing for?",
        [
            "Python Developer",
            "Java Developer",
            "AI Engineer",
            "Machine Learning Engineer",
            "Data Analyst",
            "Data Scientist",
            "GenAI Engineer",
            "Backend Developer",
        ],
    )

    experience_level = st.selectbox(
        "Your experience level",
        ["Fresher", "0-1 Years", "1-3 Years", "3-5 Years"],
    )

    difficulty = st.selectbox(
        "How tough should it be?",
        ["Easy", "Medium", "Hard"],
        index=1,
    )

    num_questions = st.slider(
        "How many questions?",
        min_value=3,
        max_value=15,
        value=5,
    )

    st.write("")
    generate = st.button(
        "Build my practice set",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# GENERATE
# --------------------------------------------------

if generate:
    with st.spinner("Putting your questions together. This takes a few seconds..."):
        try:
            st.session_state["result"] = generate_interview(
                job_role,
                experience_level,
                difficulty,
                num_questions,
            )
            st.session_state["run_id"] = st.session_state.get("run_id", 0) + 1
        except Exception as e:
            st.error(
                f"We couldn't generate your questions: {e}. "
                "Check your connection and API key, then try again."
            )


# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown(
    f"""
    <div class="hero">
        <p class="hero-greeting">{greeting()}, ready to practise?</p>
        <h1>Walk into your interview feeling prepared.</h1>
        <p>Get realistic questions, clear model answers, simple explanations and
        the follow-ups interviewers actually ask, all matched to your role.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

if "result" in st.session_state:
    result = st.session_state["result"]
    run_id = st.session_state.get("run_id", 0)
    total = len(result.questions)

    # Header card
    st.markdown(
        f"""
        <div class="result-head">
            <h2>{esc(result.job_role)}</h2>
            <div class="meta">{esc(result.experience_level)} · {total} questions ready for you</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress (counts questions marked as practised)
    done = sum(
        1 for i in range(1, total + 1)
        if st.session_state.get(f"done_{run_id}_{i}", False)
    )

    p1, p2 = st.columns([4, 1])
    with p1:
        st.progress(done / total if total else 0)
        if done == 0:
            st.caption("Open a question, practise it out loud, then tick it off.")
        elif done < total:
            st.caption(f"{done} of {total} practised. Nice momentum, keep going.")
        else:
            st.caption("All done. You've worked through the whole set. Well done! 🎉")
    with p2:
        st.download_button(
            "Save as text",
            data=build_download_text(result),
            file_name="interview_practice.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.write("")

    # Question cards
    for index, q in enumerate(result.questions, start=1):
        is_done = st.session_state.get(f"done_{run_id}_{index}", False)
        prefix = "✅ " if is_done else ""

        with st.expander(
            f"{prefix}Q{index}. {q.question}",
            expanded=(index == 1),
        ):
            st.markdown(
                f'<span class="badge badge-type">{esc(q.question_type)}</span>'
                f"{difficulty_badge(q.difficulty)}",
                unsafe_allow_html=True,
            )
            st.write("")

            tab_answer, tab_simple, tab_example, tab_follow = st.tabs(
                ["Model answer", "In simple words", "Practical example", "Follow-up"]
            )

            with tab_answer:
                st.markdown(q.model_answer)
                st.write("")
                st.markdown("**Words worth using in your answer**")
                st.markdown(
                    "".join(f'<span class="chip">{esc(k)}</span>' for k in q.keywords),
                    unsafe_allow_html=True,
                )

            with tab_simple:
                st.markdown(
                    f"""
                    <div class="callout callout-teal">
                        <div class="callout-title">Think of it this way</div>
                        {esc(q.explanation)}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with tab_example:
                st.markdown(q.practical_example)

            with tab_follow:
                st.markdown(
                    f"""
                    <div class="callout callout-amber">
                        <div class="callout-title">Be ready for this next</div>
                        {esc(q.follow_up)}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.write("")
            st.checkbox(
                "I've practised this one",
                key=f"done_{run_id}_{index}",
            )

# --------------------------------------------------
# WELCOME (before first run)
# --------------------------------------------------

else:
    st.markdown("### How it works")
    c1, c2, c3 = st.columns(3)

    tiles = [
        ("🧭", "Pick your target",
         "Choose the role, your experience and how challenging you want the practice to be."),
        ("🗣️", "Practise out loud",
         "Read the question, answer in your own words, then compare with the model answer."),
        ("🔁", "Handle the follow-up",
         "Every question comes with the next thing an interviewer is likely to ask."),
    ]

    for col, (ico, title, body) in zip((c1, c2, c3), tiles):
        with col:
            st.markdown(
                f"""
                <div class="tile">
                    <div class="ico">{ico}</div>
                    <h4>{title}</h4>
                    <p>{body}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.info("Set your preferences on the left, then choose **Build my practice set**.")