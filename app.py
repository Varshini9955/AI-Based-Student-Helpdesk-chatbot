import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Page settings
st.set_page_config(
    page_title="AI Based Student Helpdesk Chatbot",
    page_icon="🎓"
)

st.title("🎓 AI Based Student Helpdesk Chatbot")
st.write(
    "Ask me about college, academics, exams, hostel, library, "
    "placements, transport and student services."
)

# Check API key
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY is missing in the .env file.")
    st.stop()


# College helpdesk information
HELPDESK_INFO = """
You are an AI Student Helpdesk Assistant.

You help students with general college-related questions.

Topics covered:

1. EXAMS
Students can ask about examination schedules, exam instructions,
hall tickets, internal examinations and semester examinations.
For exact dates and official schedules, students should check
official college notices or contact the examination department.

2. PLACEMENTS
Students can ask about placement training, recruitment drives,
placement preparation, aptitude tests, coding practice and
interview preparation.
For company-specific recruitment details, students should check
official placement-cell announcements.

3. TRANSPORT
Students can ask about college transportation, bus routes,
bus timings and transport-related services.
For exact routes and timings, students should contact the
college transport department.

4. HOSTEL
Students can ask about hostel accommodation and basic hostel
facilities.
For room allocation, rules, fees and availability, students
should contact the hostel administration.

5. LIBRARY
Students can ask about library facilities, books, study materials
and reference resources.

6. ATTENDANCE
Students can ask general questions about attendance.
For exact attendance requirements and individual attendance records,
students should check the official college system or contact the
concerned department.

7. SCHOLARSHIP
Students can ask about scholarship-related information.
For application status, eligibility and official requirements,
students should contact the college scholarship section.

8. ACADEMICS
Students can ask about courses, subjects, departments and
academic-related information.

9. STUDENT SERVICES
Students can ask about general student support and college services.

IMPORTANT:
Do not invent college-specific dates, fees, bus routes, company
names, placement percentages or official rules.
If exact information is not available, tell the student to check
the official college notice or contact the concerned department.
"""


def ask_gemini(question):

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-3.8-flash:generateContent"
    )

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    prompt = f"""
{HELPDESK_INFO}

Student's question:
{question}

Give a simple and clear answer.
If the question is about a specific date, fee, route, company,
rule or other information that is not provided above, do not
make up an answer.
"""


    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:

            result = response.json()

            return result["candidates"][0]["content"]["parts"][0]["text"]

        elif response.status_code == 503:

            return (
                "⚠️ Gemini is temporarily busy right now. "
                "Please try again in a few seconds."
            )

        elif response.status_code == 429:

            return (
                "⚠️ Too many requests were sent. "
                "Please wait a little and try again."
            )

        else:

            return (
                f"Gemini API error: {response.status_code}\n"
                f"{response.text}"
            )

    except requests.exceptions.Timeout:

        return "⚠️ The request took too long. Please try again."

    except requests.exceptions.RequestException:

        return (
            "⚠️ Unable to connect to Gemini. "
            "Please check your internet connection."
        )

    except Exception as e:

        return f"⚠️ Unexpected error: {e}"


# User input
question = st.text_input(
    "💬 Enter your question:",
    placeholder="Example: How can I prepare for placements?"
)


if st.button("Ask 🤖"):

    if question.strip():

        with st.spinner("Thinking..."):

            answer = ask_gemini(question)

        st.subheader("🤖 Helpdesk Answer")
        st.write(answer)

    else:

        st.warning("Please enter a question.")