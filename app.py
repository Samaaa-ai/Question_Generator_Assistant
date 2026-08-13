
import streamlit as st
from google import genai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Question Generator",
    page_icon="🧠",
    layout="centered"
)


# ============================================================
# GEMINI API CONFIGURATION
# ============================================================

try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

except Exception:
    st.error("Gemini API key is not configured.")
    st.info(
        "Please add GEMINI_API_KEY in Streamlit Cloud Secrets."
    )
    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("🧠 AI Question Generator Assistant")

st.write(
    "Enter a subject and a specific topic to generate "
    "topic-focused questions using Gemini AI."
)


# ============================================================
# SIDEBAR SETTINGS
# ============================================================

st.sidebar.header("⚙️ Question Settings")


# ------------------------------------------------------------
# SUBJECT
# ------------------------------------------------------------

subject = st.sidebar.text_input(
    "Subject",
    placeholder="Example: Artificial Intelligence"
)


# ------------------------------------------------------------
# TOPIC
# ------------------------------------------------------------

topic = st.sidebar.text_input(
    "Topic",
    placeholder="Example: Uninformed Search Strategies"
)


# ------------------------------------------------------------
# ACADEMIC LEVEL
# ------------------------------------------------------------

grade = st.sidebar.selectbox(
    "Academic Level",
    [
        "School",
        "Intermediate",
        "Undergraduate",
        "Postgraduate"
    ]
)


# ------------------------------------------------------------
# DIFFICULTY
# ------------------------------------------------------------

difficulty = st.sidebar.selectbox(
    "Difficulty Level",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)


# ------------------------------------------------------------
# QUESTION TYPE
# ------------------------------------------------------------

question_type = st.sidebar.selectbox(
    "Question Type",
    [
        "Multiple Choice Questions (MCQ)",
        "Short Answer Questions",
        "Long Answer Questions",
        "True or False",
        "Mixed"
    ]
)


# ------------------------------------------------------------
# NUMBER OF QUESTIONS
# ------------------------------------------------------------

number_of_questions = st.sidebar.slider(
    "Number of Questions",
    min_value=1,
    max_value=20,
    value=5
)


# ============================================================
# ADDITIONAL INSTRUCTIONS
# ============================================================

additional_instructions = st.text_area(
    "Additional Instructions (Optional)",
    placeholder=(
        "Example: Focus on exam-oriented questions, "
        "real-world applications, numerical problems, "
        "or important concepts."
    ),
    height=100
)


# ============================================================
# QUESTION GENERATION FUNCTION
# ============================================================

def generate_questions(
    subject,
    topic,
    grade,
    difficulty,
    question_type,
    number_of_questions,
    additional_instructions
):

    prompt = f"""
You are an expert academic question generator.

Your task is to generate exactly {number_of_questions}
high-quality questions based ONLY on the specific topic
provided by the user.

==================================================
INPUT INFORMATION
==================================================

Subject:
{subject}

Specific Topic:
{topic}

Academic Level:
{grade}

Difficulty Level:
{difficulty}

Question Type:
{question_type}

Additional Instructions:
{additional_instructions}

==================================================
STRICT TOPIC RULE
==================================================

The MOST IMPORTANT requirement is that every generated
question must be directly related to the exact topic:

"{topic}"

Do NOT generate general questions about the entire subject.

Do NOT introduce unrelated topics.

Do NOT replace the requested topic with another topic.

For example:

If the subject is:
Artificial Intelligence

and the topic is:
Uninformed Search Strategies

then questions must focus on concepts such as:

- State Space Search
- Breadth-First Search
- Uniform Cost Search
- Depth-Limited Search
- Iterative Deepening Search
- Blind Search
- Search trees
- Completeness
- Optimality
- Time complexity
- Space complexity

Do NOT generate questions about unrelated AI topics such as:

- Machine Learning
- Neural Networks
- Natural Language Processing
- Computer Vision
- Robotics

unless they are explicitly part of the provided topic.

==================================================
QUESTION QUALITY RULES
==================================================

1. Generate exactly {number_of_questions} questions.

2. Every question must be directly related to:
   "{topic}"

3. Match the requested academic level:
   {grade}

4. Match the requested difficulty:
   {difficulty}

5. Avoid duplicate or repetitive questions.

6. Questions should test understanding, application,
   reasoning, or important concepts rather than only
   simple memorization.

7. Use clear and grammatically correct language.

8. Do not invent concepts that are unrelated to the topic.

9. Follow the requested question type exactly.

==================================================
MCQ RULES
==================================================

If the question type is MCQ:

- Provide exactly four options.
- Options must be A, B, C and D.
- Only one option should be the correct answer.
- Clearly identify the correct answer.
- Include a brief explanation.

==================================================
SHORT ANSWER RULES
==================================================

If the question type is Short Answer:

- Generate conceptual or application-based questions.
- Provide an expected answer.
- Keep the expected answer concise.

==================================================
LONG ANSWER RULES
==================================================

If the question type is Long Answer:

- Generate descriptive or analytical questions.
- Provide important points that should be included
  in the answer.

==================================================
TRUE/FALSE RULES
==================================================

If the question type is True or False:

- Provide a clear statement.
- Clearly identify whether it is True or False.
- Provide a brief explanation.

==================================================
MIXED RULES
==================================================

If the question type is Mixed:

Generate a balanced combination of:
- MCQs
- Short Answer Questions
- Long Answer Questions
- True/False Questions

All questions must still remain strictly within:
"{topic}"

==================================================
OUTPUT FORMAT
==================================================

QUESTION 1

Question:
<question>

Options:
A. <option>
B. <option>
C. <option>
D. <option>

Correct Answer:
<answer>

Explanation:
<brief explanation>


QUESTION 2

Question:
<question>

Options:
A. <option>
B. <option>
C. <option>
D. <option>

Correct Answer:
<answer>

Explanation:
<brief explanation>


Continue until exactly {number_of_questions}
questions have been generated.

For question types where options are not applicable,
do not include an Options section.

==================================================
FINAL CHECK
==================================================

Before returning the response, verify that:

- Exactly {number_of_questions} questions are present.
- Every question belongs specifically to "{topic}".
- No unrelated subject topics were introduced.
- The requested difficulty level is followed.
- The requested question type is followed.

Return ONLY the generated questions.
"""


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()


# ============================================================
# GENERATE BUTTON
# ============================================================

if st.button(
    "✨ Generate Questions",
    use_container_width=True
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not subject.strip():

        st.warning(
            "⚠️ Please enter a subject."
        )

    elif not topic.strip():

        st.warning(
            "⚠️ Please enter a specific topic."
        )

    else:

        try:

            # ------------------------------------------------
            # GENERATE QUESTIONS
            # ------------------------------------------------

            with st.spinner(
                "🧠 Gemini is generating topic-focused questions..."
            ):

                generated_questions = generate_questions(
                    subject,
                    topic,
                    grade,
                    difficulty,
                    question_type,
                    number_of_questions,
                    additional_instructions
                )

            # ------------------------------------------------
            # DISPLAY RESULT
            # ------------------------------------------------

            st.success(
                "✅ Questions generated successfully!"
            )

            st.subheader(
                f"📚 Questions on: {topic}"
            )

            st.markdown(
                generated_questions
            )

            # ------------------------------------------------
            # DOWNLOAD
            # ------------------------------------------------

            st.download_button(
                label="⬇️ Download Questions",
                data=generated_questions,
                file_name="generated_questions.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:

            st.error(
                "❌ Question generation failed."
            )

            st.write(
                "Error:",
                str(e)
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "AI Question Generator Assistant | "
    "Powered by Gemini AI + Streamlit"
)
