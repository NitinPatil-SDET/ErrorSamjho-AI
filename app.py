import streamlit as st

from ai_service import explain_error


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="ErrorSamjho AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .main-title {
            font-size: 42px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 5px;
        }

        .sub-title {
            font-size: 18px;
            color: #666666;
            text-align: center;
            margin-bottom: 30px;
        }

        .info-box {
            background-color: #f0f7ff;
            border-left: 5px solid #1f77b4;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }

        .footer {
            text-align: center;
            color: #777777;
            font-size: 13px;
            margin-top: 40px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.header("About ErrorSamjho AI")

    st.write(
        """
        ErrorSamjho AI technical error logs ko analyze karke
        simple Hindi mein explain karta hai.
        """
    )

    st.subheader("Supported Errors")

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
        2. **Explain Error** button click karein.
        3. AI-generated analysis dekhein.
        4. Solution apply karne se pehle validate karein.
        """
    )

    st.divider()

    st.warning(
        "Passwords, API keys, tokens aur confidential data "
        "paste karne se pehle remove ya mask karein."
    )


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🔍 ErrorSamjho AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="sub-title">
        Technical errors ko simple Hindi mein samjho
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="info-box">
        Apna error message, stack trace ya application log niche paste karein.
        ErrorSamjho AI error ka meaning, root cause, fix aur prevention
        steps provide karega.
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = ""

if "submitted_error" not in st.session_state:
    st.session_state.submitted_error = ""


# ---------------------------------------------------------
# SAMPLE ERRORS
# ---------------------------------------------------------

sample_errors = {
    "Select a sample error": "",
    "Python Package Error": (
        "ModuleNotFoundError: No module named 'openai'"
    ),
    "Selenium Element Error": (
        "selenium.common.exceptions.NoSuchElementException: "
        "Unable to locate element using XPath "
        "//button[@id='upload']"
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


selected_sample = st.selectbox(
    "Try a sample error",
    options=list(sample_errors.keys()),
)


# ---------------------------------------------------------
# ERROR INPUT
# ---------------------------------------------------------

default_error = sample_errors[selected_sample]

error_log = st.text_area(
    label="Paste your error log",
    value=default_error,
    height=280,
    placeholder=(
        "Example:\n\n"
        "Traceback (most recent call last):\n"
        '  File "app.py", line 1, in <module>\n'
        "    from openai import OpenAI\n"
        "ModuleNotFoundError: No module named 'openai'"
    ),
    help=(
        "Paste the complete error message or stack trace. "
        "Remove passwords, API keys and confidential details."
    ),
)


# ---------------------------------------------------------
# INPUT INFORMATION
# ---------------------------------------------------------

character_count = len(error_log)
line_count = len(error_log.splitlines()) if error_log else 0

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.caption(f"Characters: {character_count}")

with info_col2:
    st.caption(f"Lines: {line_count}")


# ---------------------------------------------------------
# ACTION BUTTONS
# ---------------------------------------------------------

button_col1, button_col2 = st.columns([1, 1])

with button_col1:
    explain_button = st.button(
        "🔍 Explain Error",
        type="primary",
        use_container_width=True,
    )

with button_col2:
    clear_button = st.button(
        "🗑️ Clear Result",
        use_container_width=True,
    )


# ---------------------------------------------------------
# CLEAR ACTION
# ---------------------------------------------------------

if clear_button:
    st.session_state.analysis_result = ""
    st.session_state.submitted_error = ""
    st.rerun()


# ---------------------------------------------------------
# EXPLAIN ERROR ACTION
# ---------------------------------------------------------

if explain_button:

    cleaned_error_log = error_log.strip()

    if not cleaned_error_log:
        st.warning(
            "Please paste an error log before clicking Explain Error."
        )

    elif len(cleaned_error_log) < 10:
        st.warning(
            "The entered error is too short. "
            "Please provide a complete error message."
        )

    else:
        st.session_state.submitted_error = cleaned_error_log

        try:
            with st.spinner(
                "ErrorSamjho AI error analyze kar raha hai..."
            ):
                result = explain_error(cleaned_error_log)

            st.session_state.analysis_result = result
            st.success("Error analysis completed successfully.")

        except ValueError as error:
            st.session_state.analysis_result = ""
            st.error(f"Input or response error: {error}")

        except RuntimeError as error:
            st.session_state.analysis_result = ""
            st.error(f"AI service error: {error}")

        except Exception as error:
            st.session_state.analysis_result = ""
            st.error(
                "An unexpected error occurred while analyzing the log."
            )

            with st.expander("Technical error details"):
                st.code(str(error))


# ---------------------------------------------------------
# DISPLAY AI RESULT
# ---------------------------------------------------------

if st.session_state.analysis_result:

    st.divider()

    st.subheader("Error Analysis")

    st.markdown(st.session_state.analysis_result)

    st.divider()

    st.download_button(
        label="⬇️ Download Analysis",
        data=st.session_state.analysis_result,
        file_name="errorsamjho_analysis.txt",
        mime="text/plain",
        use_container_width=True,
    )


# ---------------------------------------------------------
# DISCLAIMER
# ---------------------------------------------------------

st.info(
    "AI-generated solution ko production environment mein apply "
    "karne se pehle validate karein."
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        ErrorSamjho AI | Built using Python, Streamlit, Groq and Llama
    </div>
    """,
    unsafe_allow_html=True,
)