import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="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")

# OpenAI API Key
  # Replace with your OpenAI key

# Set page configuration
st.set_page_config(page_title="Porter's Five Forces Facilitator", layout="wide")

# Title of the app
st.title("Porter's Five Forces Analysis - Team Collaboration Facilitator")

# Description of the app
st.markdown("""
Welcome to the Porter's Five Forces Analysis facilitator tool! This app will guide your team through a structured analysis of your case study, encouraging in-depth discussion and collaboration. Let's get started!
""")

# Input for team name and case study
with st.sidebar:
    st.header("Team and Case Information")
    team_name = st.text_input("Enter your team name:")
    case_study = st.text_input("Enter the name of your case study:")
    start_analysis = st.button("Start Analysis")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
if "analysis" not in st.session_state:
    st.session_state.analysis = {
        "Competitive Rivalry": "",
        "Threat of New Entrants": "",
        "Bargaining Power of Suppliers": "",
        "Bargaining Power of Buyers": "",
        "Threat of Substitutes": ""
    }
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "system", "content": "You are a helpful assistant specialized in Porter's Five Forces. Act as a facilitator to guide the team through each force, asking probing questions based on their inputs."}
    ]

# Function to display open-ended questions
def display_questions(force_name, questions):
    st.subheader(force_name)
    st.write("Consider the following questions:")
    for q in questions:
        st.markdown(f"- {q}")
    response = st.text_area(f"Team's insights on {force_name}", st.session_state.analysis[force_name], height=150)
    st.session_state.analysis[force_name] = response

# Function to handle chatbot interaction
def chatbot_interaction(force_name):
    st.write("### Chatbot Facilitator")
    user_input = st.text_input("Ask the chatbot for guidance or clarification:")
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})

        # Include the team's analysis in the assistant's context
        context = "\n".join([f"{key}: {value}" for key, value in st.session_state.analysis.items()])
        st.session_state.chat_messages.append({"role": "system", "content": f"Current Analysis:\n{context}"})

        # Get the chatbot's response
        response = client.chat.completions.create(model="gpt-4",  # Use "gpt-4" if you have access
        messages=st.session_state.chat_messages)

        chatbot_reply = response.choices[0].message.content
        st.session_state.chat_messages.append({"role": "assistant", "content": chatbot_reply})
        st.session_state.chat_history.append({"user": user_input, "assistant": chatbot_reply})

        # Display the chatbot's response
        st.write(f"**Chatbot**: {chatbot_reply.strip()}")

    # Display chat history
    if st.session_state.chat_history:
        st.write("### Chat History")
        for chat in st.session_state.chat_history:
            st.write(f"**You**: {chat['user']}")
            st.write(f"**Chatbot**: {chat['assistant']}")

# Sequential workflow through the Five Forces
if start_analysis and team_name and case_study:
    st.write(f"### Team **{team_name}** is analyzing the **{case_study}** case.")
    forces = [
        ("Competitive Rivalry", [
            "Who are the main competitors in the industry?",
            "What market share do they hold?",
            "How does their product/service quality compare?"
        ]),
        ("Threat of New Entrants", [
            "What are the barriers to entry?",
            "Are there high startup costs or regulations?",
            "How difficult is it for new competitors to enter the market?"
        ]),
        ("Bargaining Power of Suppliers", [
            "How many suppliers are available?",
            "How unique is the supplier's product or service?",
            "Can suppliers dictate terms or prices?"
        ]),
        ("Bargaining Power of Buyers", [
            "How many buyers are there?",
            "Can buyers easily switch to competitors?",
            "How sensitive are buyers to price changes?"
        ]),
        ("Threat of Substitutes", [
            "Are there alternative products or services?",
            "How easily can customers switch to substitutes?",
            "What is the price-performance trade-off of substitutes?"
        ])
    ]

    if st.session_state.step < len(forces):
        force_name, questions = forces[st.session_state.step]
        display_questions(force_name, questions)
        if st.button("Next", key=f"next_{st.session_state.step}"):
            st.session_state.step += 1
    else:
        st.success("You have completed the analysis of all five forces!")
        st.write("### Summary of Your Analysis:")
        for force, analysis in st.session_state.analysis.items():
            st.write(f"**{force}**: {analysis}")

        # Chatbot interaction after completing all forces
        chatbot_interaction("Summary")

        # Downloadable report
        analysis_report = f"Porter's Five Forces Analysis for Team {team_name} - {case_study} Case Study\n\n"
        for force, analysis in st.session_state.analysis.items():
            analysis_report += f"{force}:\n{analysis}\n\n"
        st.download_button("Download Full Analysis", analysis_report, file_name="porters_five_forces_analysis.txt")

else:
    st.warning("Please enter your team name and case study to begin the analysis.")

# Footer with facilitator resources (optional)
with st.expander("Facilitator Resources"):
    st.write("""
    **Tips for Effective Team Discussions:**
    - Encourage every team member to share their thoughts.
    - Respect different perspectives and build upon ideas.
    - Keep discussions focused on the current force before moving to the next.
    - Use the chatbot facilitator to delve deeper into any aspect.
    """)
