# ErrorSamjho AI

ErrorSamjho AI is an AI-powered technical error analysis tool that explains error logs in simple Hindi written using English letters.

The application detects the likely cause of an error and provides structured troubleshooting steps.

## Current Features

- Paste technical errors and stack traces
- Get explanations in simple Hindi
- Identify likely root causes
- Receive step-by-step fixes
- View corrected commands or code where applicable
- Download the analysis as a text file
- Try sample Python, Selenium, SMTP, SQL and file-processing errors
- Secure API configuration using environment variables

## Supported Error Types

- Python
- Selenium
- Java
- SQL
- SMTP
- API
- AutomationEdge
- Database
- Network
- File processing

## Technology Stack

- Python
- Streamlit
- Groq API
- Llama 3.3 70B
- OpenAI-compatible Python SDK

## Project Structure

```text
ErrorSamjoAI/
├── app.py
├── ai_service.py
├── connection.py
├── prompt.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md