import time

import streamlit as st

from ai_service import RateLimiter, explain_error
from connection import (
    API_REQUEST_COOLDOWN_SECONDS,
    DUPLICATE_REQUEST_WINDOW_SECONDS,
    MAX_SESSION_REQUESTS,
)

st.set_page_config(
    page_title="ErrorSamjho AI",
    page_icon="🔍",
    layout="wide",
    #initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
        --page: #f4f8fa;
        --panel: #ffffff;
        --navy: #102a43;
        --navy-hover: #0b2035;
        --teal: #087f8c;
        --teal-hover: #066a75;
        --teal-soft: #e7f5f6;
        --text: #101828;
        --muted: #475467;
        --border: #98a2b3;
        --disabled: #d7dee8;
        --disabled-text: #475467;
        --info-bg: #eaf2fb;
        --info-text: #173b63;
        --success-bg: #eaf7ef;
        --success-text: #17643a;
        --warning-bg: #fff6df;
        --warning-text: #6b4f00;
        --error-bg: #fdecec;
        --error-text: #8a1c1c;
        --shadow: rgba(16, 42, 67, 0.12);
    }

    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: var(--page) !important;
        color: var(--text) !important;
    }

    [data-testid="stHeader"] {
        background: var(--page) !important;
        z-index: 1000 !important;
    }

    [data-testid="stDecoration"] { display: none !important; }

    .main .block-container,
    [data-testid="stMainBlockContainer"] {
        max-width: 1200px;
        padding-top: 4rem;
        padding-bottom: 2rem;
    }

    /* Main typography */
    [data-testid="stMain"] .stMarkdown,
    [data-testid="stMain"] .stMarkdown p,
    [data-testid="stMain"] .stMarkdown li,
    [data-testid="stMain"] .stMarkdown h1,
    [data-testid="stMain"] .stMarkdown h2,
    [data-testid="stMain"] .stMarkdown h3,
    [data-testid="stMain"] .stMarkdown h4,
    [data-testid="stMain"] .stMarkdown h5,
    [data-testid="stMain"] .stMarkdown h6,
    [data-testid="stMain"] label,
    [data-testid="stMain"] label p,
    [data-testid="stMain"] [data-testid="stCaptionContainer"],
    [data-testid="stMain"] [data-testid="stCaptionContainer"] p,
    [data-testid="stMain"] [data-testid="stMetricLabel"],
    [data-testid="stMain"] [data-testid="stMetricValue"] {
        color: var(--text) !important;
    }

    .main-title {
        color: var(--navy) !important;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.35rem;
        width: 100%;
        max-width: 100%;
        font-size: clamp(1.9rem, 5vw, 3.4rem);
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: 0;
        overflow: visible;
        overflow-wrap: anywhere;
        margin: 0 0 0.35rem;
    }

    .sub-title {
        color: var(--teal) !important;
        font-size: 1.1rem;
        font-weight: 650;
        margin: 0 0 1.5rem;
    }

    .info-card {
        background: var(--panel) !important;
        color: var(--text) !important;
        border: 1px solid #d0d5dd !important;
        border-left: 6px solid var(--teal) !important;
        border-radius: 12px;
        box-shadow: 0 8px 24px var(--shadow);
        padding: 1rem 1.1rem;
        margin-bottom: 1.5rem;
    }

    .footer {
        color: var(--muted) !important;
        text-align: center;
        font-size: 0.84rem;
        font-weight: 600;
        margin-top: 2.4rem;
    }

    a, .stMarkdown a, .footer a {
        color: var(--teal) !important;
        text-decoration: underline !important;
        text-underline-offset: 3px;
        font-weight: 700;
    }

    a:hover, a:focus, a:active, a:visited {
        color: var(--teal-hover) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"] {
        background: var(--navy) !important;
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] {
        border-right: 3px solid var(--teal) !important;
    }

    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] label p,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMetricLabel"],
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.30) !important;
    }

    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="collapsedControl"] button,
    [data-testid="collapsedControl"] svg {
        color: var(--teal) !important;
        fill: var(--teal) !important;
    }

    [data-testid="stMain"] hr { border-color: #d0d5dd !important; }

    /* Labels, captions and help text */
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    [data-testid="InputInstructions"],
    [data-testid="InputInstructions"] span,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color: var(--text) !important;
        opacity: 1 !important;
    }

    /* Text inputs */
    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {
        background: #ffffff !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
        caret-color: var(--teal) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        box-shadow: none !important;
        opacity: 1 !important;
    }

    [data-testid="stTextArea"] textarea {
        min-height: 260px !important;
        font-size: 1rem !important;
    }

    [data-testid="stTextArea"] textarea::placeholder,
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stNumberInput"] input::placeholder {
        color: var(--muted) !important;
        -webkit-text-fill-color: var(--muted) !important;
        opacity: 1 !important;
    }

    [data-testid="stTextArea"] textarea:hover,
    [data-testid="stTextInput"] input:hover,
    [data-testid="stNumberInput"] input:hover {
        border-color: var(--teal) !important;
    }

    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus {
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 3px var(--teal-soft) !important;
        outline: none !important;
    }

    [data-testid="stTextArea"] textarea:disabled,
    [data-testid="stTextInput"] input:disabled {
        background: var(--disabled) !important;
        color: var(--disabled-text) !important;
        -webkit-text-fill-color: var(--disabled-text) !important;
    }

    /* Select box and opened options */
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    [data-testid="stSelectbox"] [role="combobox"] {
        background: #ffffff !important;
        color: var(--text) !important;
        border-color: var(--border) !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 3px var(--teal-soft) !important;
    }

    [data-testid="stSelectbox"] span,
    [data-testid="stSelectbox"] input,
    [data-testid="stSelectbox"] svg {
        color: var(--text) !important;
        fill: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    ul[role="listbox"] {
        background: #ffffff !important;
        color: var(--text) !important;
        border-color: var(--teal) !important;
    }

    li[role="option"], div[role="option"],
    li[role="option"] > div, div[role="option"] > div {
        background: #ffffff !important;
        color: var(--text) !important;
    }

    li[role="option"]:hover, div[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"] {
        background: var(--teal-soft) !important;
        color: var(--navy) !important;
    }

    /* Buttons */
    [data-testid="stButton"] > button,
    [data-testid="stDownloadButton"] > button,
    [data-testid="stFormSubmitButton"] > button {
        min-height: 2.9rem !important;
        border-radius: 10px !important;
        font-weight: 750 !important;
        box-shadow: 0 6px 16px var(--shadow) !important;
        opacity: 1 !important;
        transition: background-color .15s ease, transform .15s ease !important;
    }

    [data-testid="stButton"] > button[kind="secondary"] {
        background: #ffffff !important;
        color: var(--teal) !important;
        border: 2px solid var(--teal) !important;
    }

    [data-testid="stButton"] > button[kind="secondary"] p,
    [data-testid="stButton"] > button[kind="secondary"] span,
    [data-testid="stButton"] > button[kind="secondary"] svg {
        color: var(--teal) !important;
        fill: var(--teal) !important;
    }

    [data-testid="stButton"] > button[kind="secondary"]:hover,
    [data-testid="stButton"] > button[kind="secondary"]:focus,
    [data-testid="stButton"] > button[kind="secondary"]:active {
        background: var(--teal-soft) !important;
        color: var(--teal-hover) !important;
        border-color: var(--teal-hover) !important;
        outline: 2px solid var(--teal) !important;
        outline-offset: 2px;
    }

    [data-testid="stButton"] > button[kind="primary"],
    [data-testid="stFormSubmitButton"] > button {
        background: var(--teal) !important;
        color: #ffffff !important;
        border: 2px solid var(--teal) !important;
    }

    [data-testid="stButton"] > button[kind="primary"] p,
    [data-testid="stButton"] > button[kind="primary"] span,
    [data-testid="stButton"] > button[kind="primary"] svg,
    [data-testid="stFormSubmitButton"] > button p,
    [data-testid="stFormSubmitButton"] > button span,
    [data-testid="stFormSubmitButton"] > button svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    [data-testid="stButton"] > button[kind="primary"]:hover,
    [data-testid="stButton"] > button[kind="primary"]:focus,
    [data-testid="stButton"] > button[kind="primary"]:active,
    [data-testid="stFormSubmitButton"] > button:hover,
    [data-testid="stFormSubmitButton"] > button:focus,
    [data-testid="stFormSubmitButton"] > button:active {
        background: var(--teal-hover) !important;
        border-color: var(--teal-hover) !important;
        outline: 2px solid var(--teal) !important;
        outline-offset: 2px;
    }

    [data-testid="stDownloadButton"] > button {
        background: var(--navy) !important;
        color: #ffffff !important;
        border: 2px solid var(--navy) !important;
    }

    [data-testid="stDownloadButton"] > button p,
    [data-testid="stDownloadButton"] > button span,
    [data-testid="stDownloadButton"] > button svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    [data-testid="stDownloadButton"] > button:hover,
    [data-testid="stDownloadButton"] > button:focus,
    [data-testid="stDownloadButton"] > button:active {
        background: var(--navy-hover) !important;
        border-color: var(--navy-hover) !important;
        outline: 2px solid var(--navy) !important;
        outline-offset: 2px;
    }

    [data-testid="stButton"] > button:disabled,
    [data-testid="stDownloadButton"] > button:disabled,
    [data-testid="stFormSubmitButton"] > button:disabled {
        background: var(--disabled) !important;
        color: var(--disabled-text) !important;
        border: 2px solid var(--border) !important;
        cursor: not-allowed !important;
        box-shadow: none !important;
        opacity: 1 !important;
        outline: none !important;
    }

    [data-testid="stButton"] > button:disabled p,
    [data-testid="stButton"] > button:disabled span,
    [data-testid="stButton"] > button:disabled svg,
    [data-testid="stDownloadButton"] > button:disabled p,
    [data-testid="stDownloadButton"] > button:disabled span,
    [data-testid="stDownloadButton"] > button:disabled svg {
        color: var(--disabled-text) !important;
        fill: var(--disabled-text) !important;
    }

    /* Alerts: readable semantic colors with labels in message text */
    [data-testid="stAlert"],
    [data-testid="stNotification"] {
        background: var(--info-bg) !important;
        color: var(--info-text) !important;
        border: 1px solid var(--info-text) !important;
        border-left: 5px solid var(--info-text) !important;
        border-radius: 10px !important;
        box-shadow: 0 5px 14px var(--shadow) !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] li,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] svg,
    [data-testid="stNotification"] p,
    [data-testid="stNotification"] span,
    [data-testid="stNotification"] svg {
        color: inherit !important;
        fill: currentColor !important;
    }

    [data-testid="stAlert"][kind="positive"],
    [data-baseweb="notification"][kind="positive"] {
        background: var(--success-bg) !important;
        color: var(--success-text) !important;
        border-color: var(--success-text) !important;
    }

    [data-testid="stAlert"][kind="warning"],
    [data-baseweb="notification"][kind="warning"] {
        background: var(--warning-bg) !important;
        color: var(--warning-text) !important;
        border-color: var(--warning-text) !important;
    }

    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background: #fff1c2 !important;
        color: #5f4300 !important;
        border: 1px solid #d99a00 !important;
        border-left: 5px solid #d99a00 !important;
    }

    [data-testid="stSidebar"] [data-testid="stAlert"] p,
    [data-testid="stSidebar"] [data-testid="stAlert"] span,
    [data-testid="stSidebar"] [data-testid="stAlert"] svg {
        color: #5f4300 !important;
        fill: #5f4300 !important;
    }

    [data-testid="stAlert"][kind="negative"],
    [data-baseweb="notification"][kind="negative"] {
        background: var(--error-bg) !important;
        color: var(--error-text) !important;
        border-color: var(--error-text) !important;
    }

    /* Result card and generated Markdown */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important;
        color: var(--text) !important;
        border: 2px solid var(--teal) !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 28px var(--shadow) !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown,
    [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown p,
    [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown li,
    [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h1,
    [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h2,
    [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h3,
    [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h4 {
        color: var(--text) !important;
    }

    .stMarkdown :not(pre) > code {
        background: var(--teal-soft) !important;
        color: var(--navy) !important;
        border: 1px solid var(--teal) !important;
        border-radius: 4px !important;
    }

    .stMarkdown pre,
    .stMarkdown pre code,
    [data-testid="stCodeBlock"],
    [data-testid="stCodeBlock"] pre,
    [data-testid="stCodeBlock"] code {
        background: var(--navy) !important;
        color: #ffffff !important;
    }

    .stMarkdown pre, [data-testid="stCodeBlock"] {
        border: 2px solid var(--teal) !important;
        border-radius: 10px !important;
    }

    [data-testid="stCodeBlock"] button,
    [data-testid="stCodeBlock"] button svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    /* Expander and tooltip */
    [data-testid="stExpander"] {
        background: #ffffff !important;
        color: var(--text) !important;
        border: 1.5px solid var(--teal) !important;
        border-radius: 10px !important;
    }

    [data-testid="stExpander"] details,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary svg {
        background: #ffffff !important;
        color: var(--text) !important;
        fill: var(--text) !important;
    }

    div[data-baseweb="tooltip"],
    div[data-baseweb="tooltip"] > div,
    [role="tooltip"] {
        background: var(--navy) !important;
        color: #ffffff !important;
        border: 1px solid var(--teal-soft) !important;
    }

    div[data-baseweb="tooltip"] p,
    div[data-baseweb="tooltip"] span,
    [role="tooltip"] p,
    [role="tooltip"] span { color: #ffffff !important; }

    [data-testid="stSpinner"] p,
    [data-testid="stSpinner"] span { color: var(--navy) !important; }

    [data-testid="stSpinner"] svg,
    [data-testid="stSpinner"] svg * {
        color: var(--teal) !important;
        fill: var(--teal) !important;
        stroke: var(--teal) !important;
    }

    @media (prefers-color-scheme: dark) {
        html, body, .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background: var(--page) !important;
            color: var(--text) !important;
        }
    }

    @media (max-width: 768px) {
        .main .block-container,
        [data-testid="stMainBlockContainer"] {
            padding: 3.5rem 1rem 1rem !important;
        }
        .main-title { font-size: clamp(1.75rem, 8vw, 2.15rem); }
        .info-card { padding: 0.9rem 1rem; }
        [data-testid="stHorizontalBlock"] { gap: 0.7rem !important; }
        [data-testid="stButton"] > button,
        [data-testid="stDownloadButton"] > button { width: 100% !important; }
        [data-testid="stTextArea"] textarea { min-height: 220px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session state
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = ""
if "submitted_error" not in st.session_state:
    st.session_state.submitted_error = ""
if "request_count" not in st.session_state:
    st.session_state.request_count = 0
if "request_cache" not in st.session_state:
    st.session_state.request_cache = {}
if "last_api_request_time" not in st.session_state:
    st.session_state.last_api_request_time = 0.0
if "last_submission_time" not in st.session_state:
    st.session_state.last_submission_time = 0.0
if "last_submission_value" not in st.session_state:
    st.session_state.last_submission_value = ""
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
if "api_rate_limiter" not in st.session_state:
    st.session_state.api_rate_limiter = RateLimiter(max_calls=3, window_seconds=60)

with st.sidebar:
    st.header("About ErrorSamjho AI")
    st.write(
        "ErrorSamjho AI technical error logs ko analyze karke "
        "simple Hindi mein explain karta hai."
    )
    st.metric(
        label="Requests left this session",
        value=max(MAX_SESSION_REQUESTS - st.session_state.request_count, 0),
    )
    st.caption(f"Session limit: {MAX_SESSION_REQUESTS} requests")
    st.divider()
    st.subheader("Supported Error Types")
    st.markdown(
        """
        - Python
        - Selenium
        - SQL
        - SMTP
        - API
        - Java
        - AutomationEdge
        - File Processing
        - Database
        - Network
        """
    )
    st.divider()
    st.subheader("How to Use")
    st.markdown(
        """
        1. Error log paste karein.
        2. Explain Error button click karein.
        3. AI-generated analysis dekhein.
        4. Fix apply karne se pehle validate karein.
        """
    )
    st.divider()
    st.warning(
        "WARNING: Passwords, API keys, tokens, and sensitive data ko remove "
        "ya mask kar ke hi paste karein."
    )

st.markdown('<div class="main-title">🔍 ErrorSamjho AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Technical errors ko simple Hindi mein samjho.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="info-card">
        <strong>QUICK START:</strong> Apna error message, stack trace, ya application
        log niche paste karein. ErrorSamjho AI error ka meaning, root cause, fix aur
        prevention tips provide karega.
    </div>
    """,
    unsafe_allow_html=True,
)

sample_errors = {
    "Select a sample error": "",
    "Python Package Error": "ModuleNotFoundError: No module named 'openai'",
    "Selenium Element Error": (
        "selenium.common.exceptions.NoSuchElementException: "
        "Unable to locate element using XPath //button[@id='upload']"
    ),
    "File Not Found Error": (
        "FileNotFoundError: [Errno 2] No such file or directory: "
        "'C:\\Input\\bank_statement.xlsx'"
    ),
    "SMTP Authentication Error": (
        "smtplib.SMTPAuthenticationError: "
        "(535, b'5.7.8 Username and Password not accepted')"
    ),
    "SQL Table Error": (
        "AnalysisException: Table or view not found: "
        "prod_gold.downstream.customer_data"
    ),
}

selected_sample = st.selectbox("Try a sample error", options=list(sample_errors.keys()))
default_error = sample_errors[selected_sample]

error_log = st.text_area(
    label="Paste your error log",
    value=default_error,
    height=260,
    placeholder=(
        "Example:\n\n"
        "Traceback (most recent call last):\n"
        '  File "app.py", line 1, in <module>\n'
        "    from openai import OpenAI\n"
        "ModuleNotFoundError: No module named 'openai'"
    ),
    help=(
        "Paste the complete error message or stack trace. Remove passwords, "
        "API keys, and confidential details before sharing."
    ),
)

character_count = len(error_log)
line_count = len(error_log.splitlines()) if error_log else 0
info_col1, info_col2, info_col3 = st.columns([1, 1, 2])
with info_col1:
    st.caption(f"Characters: {character_count}")
with info_col2:
    st.caption(f"Lines: {line_count}")
with info_col3:
    st.caption(
        f"Remaining requests: {max(MAX_SESSION_REQUESTS - st.session_state.request_count, 0)}"
    )

button_col1, button_col2 = st.columns([1.2, 1])
with button_col1:
    explain_disabled = (
        st.session_state.is_processing
        or st.session_state.request_count >= MAX_SESSION_REQUESTS
    )
    explain_button = st.button(
        "🔍 Error Samjho",
        type="primary",
        use_container_width=True,
        disabled=explain_disabled,
    )
with button_col2:
    clear_button = st.button(
        "Clear Result",
        type="secondary",
        use_container_width=True,
    )

if clear_button:
    st.session_state.analysis_result = ""
    st.session_state.submitted_error = ""
    st.rerun()

if explain_button:
    cleaned_error_log = error_log.strip()
    duplicate_window_elapsed = time.monotonic() - st.session_state.last_submission_time
    same_error_recently_submitted = (
        cleaned_error_log
        and cleaned_error_log == st.session_state.last_submission_value
        and duplicate_window_elapsed < DUPLICATE_REQUEST_WINDOW_SECONDS
    )

    if not cleaned_error_log:
        st.warning("WARNING: Please paste an error log before clicking Explain Error.")
    elif len(cleaned_error_log) < 10:
        st.warning("WARNING: The entered error is too short. Please provide a complete error message.")
    elif len(cleaned_error_log) > 20000:
        st.warning("WARNING: The error log is too large. Keep the input under 20,000 characters.")
    elif st.session_state.request_count >= MAX_SESSION_REQUESTS:
        st.warning(
            "LIMIT REACHED: Please refresh or try again later. "
            "Your current session has used all available requests."
        )
    elif same_error_recently_submitted:
        st.warning(
            "DUPLICATE REQUEST: This exact error was submitted recently. "
            "Please wait before submitting it again."
        )
    elif time.monotonic() - st.session_state.last_api_request_time < API_REQUEST_COOLDOWN_SECONDS:
        remaining_wait = max(
            0,
            API_REQUEST_COOLDOWN_SECONDS
            - (time.monotonic() - st.session_state.last_api_request_time),
        )
        st.warning(
            f"COOLDOWN: Please wait about {int(remaining_wait) + 1} seconds "
            "before the next request."
        )
    else:
        cache_key = cleaned_error_log
        if cache_key in st.session_state.request_cache:
            st.session_state.analysis_result = st.session_state.request_cache[cache_key]
            st.session_state.submitted_error = cleaned_error_log
            st.success(
                "CACHED RESULT: This exact error was already analyzed in this "
                "session. Showing the saved analysis."
            )
        else:
            st.session_state.is_processing = True
            st.session_state.submitted_error = cleaned_error_log
            st.session_state.last_submission_value = cleaned_error_log
            st.session_state.last_submission_time = time.monotonic()
            try:
                with st.spinner("Analyzing your error log. Please wait."):
                    result = explain_error(
                        cleaned_error_log,
                        rate_limiter=st.session_state.api_rate_limiter,
                    )
                st.session_state.analysis_result = result
                st.session_state.request_cache[cache_key] = result
                st.session_state.request_count += 1
                st.session_state.last_api_request_time = time.monotonic()
                st.success("SUCCESS: Error analysis completed successfully.")
            except RuntimeError as error:
                st.session_state.analysis_result = ""
                st.warning(f"SERVICE WARNING: {error}")
            except ValueError as error:
                st.session_state.analysis_result = ""
                st.error(f"INPUT ERROR: Validation failed: {error}")
            except Exception as error:
                st.session_state.analysis_result = ""
                st.error("API ERROR: An unexpected error occurred while analyzing the log.")
                with st.expander("Technical error details"):
                    st.code(str(error))
            finally:
                st.session_state.is_processing = False

if st.session_state.analysis_result:
    st.divider()
    with st.container(border=True):
        st.subheader("Error Analysis")
        st.markdown(st.session_state.analysis_result)
    st.download_button(
        label="Download Analysis",
        data=st.session_state.analysis_result,
        file_name="errorsamjho_analysis.txt",
        mime="text/plain",
        use_container_width=True,
    )

st.info(
    "INFORMATION: AI-generated guidance ko production environment mein apply "
    "karne se pehle validate karein."
)

st.markdown(
    """
    <div class="footer">
        ErrorSamjho AI | Made By
        <a href="https://www.linkedin.com/in/nitinpatilsdet/"
           target="_blank" rel="noopener noreferrer">Nitin Patil</a>
    </div>
    """,
    unsafe_allow_html=True,
)
