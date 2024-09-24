import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="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")

# OpenAI API Key (replace with your actual OpenAI key)
  # Replace with your OpenAI key

# Configure Streamlit page layout
st.set_page_config(page_title="Porter's Five Forces AI Analysis", layout="wide")

# Title of the app
st.title("Porter's Five Forces Analysis - AI Guided Tool")

# Description of the app
st.write("""
Welcome to the Porter's Five Forces Analysis AI-Guided Tool! This app allows your team to analyze each of the five forces, rate them, and receive AI-guided feedback and industry-specific insights based on the business case you are analyzing.
""")

# Session state variables to keep track of conversation and inputs
if "analysis_started" not in st.session_state:
    st.session_state.analysis_started = False
if "messages" not in st.session_state:
    # Custom GPT priming message to act as an expert in Porter's Five Forces
    st.session_state.messages = [
        {"role": "system", "content": """
        You are an expert in guiding students through Porter’s Five Forces framework. Your role is to help students apply this model to analyze a business case. For each force (Competitive Rivalry, Threat of New Entrants, Bargaining Power of Suppliers, Bargaining Power of Buyers, and Threat of Substitutes), you will guide them by asking targeted questions, prompting critical thinking, and offering case-specific and industry-specific insights. 
        Avoid unrelated topics and keep the discussion focused on Porter’s Five Forces. Encourage students to reflect on their analysis and challenge their assumptions when necessary.
        """}
    ]
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Function to display force-specific prompts, collect ratings, generate AI feedback, and provide a chat section
def display_force_section(force_name, prompt_questions, slider_label, ai_follow_up_prompt, case_study):
    st.header(force_name)
    st.write(f"**Questions to consider when discussing {force_name}:**")
    for question in prompt_questions:
        st.write(f"- {question}")

    rating = st.slider(slider_label, 1, 10)

    # Industry-Specific Prompt
    industry_specific_prompt = f"Based on the case study of {case_study}, provide additional insights for analyzing {force_name}."

    # AI follow-up question based on rating
    st.write("### AI Feedback and Follow-up Question")
    response = client.chat.completions.create(model="gpt-3.5-turbo",  # Or "gpt-4" if available
    messages=st.session_state.messages + [
        {"role": "user", "content": ai_follow_up_prompt.format(rating)},
        {"role": "user", "content": industry_specific_prompt}
    ])
    ai_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    st.write(f"**AI**: {ai_reply.strip()}")

    # Chat section to ask follow-up questions about this specific force
    st.write("### Ask the AI about this force")
    user_input = st.text_input(f"Ask a question related to {force_name}")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Or "gpt-4" if available
        messages=st.session_state.messages)
        ai_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        st.write(f"**AI**: {ai_reply.strip()}")

    return rating

# Introduction for team setup
team_name = st.text_input("Enter your team name:")
case_study = st.text_input("What is the name of the strategy case you are working on?")

if team_name and case_study:
    st.write(f"Great! Team **{team_name}** is analyzing the **{case_study}** case.")

# Step-by-step guidance for each force
if st.button("Start Porter’s Five Forces Analysis"):
    st.session_state.analysis_started = True

if st.session_state.analysis_started:
    st.subheader("Step-by-Step Discussion of Porter’s Five Forces")

    # Force-by-Force Analysis Sections with AI integration and chat for each force

    # Competitive Rivalry
    competitive_rivalry = display_force_section(
        "1. Competitive Rivalry", 
        [
            "Who are the key competitors in this industry?",
            "How do these competitors differentiate themselves in terms of pricing, product features, or services?",
            "What market share do the top competitors hold, and how is it changing?",
            "How intense is the competition in terms of marketing, innovation, and customer acquisition?",
            "Are there high exit barriers (e.g., specialized assets, fixed costs) that make it difficult for competitors to leave the market?"
        ], 
        "Rate the intensity of competition",
        "You rated Competitive Rivalry as {}. Why do you believe competition is at this level, and are there external factors (e.g., technological advancements or market share shifts) that might influence this rating?",
        case_study
    )

    # Threat of New Entrants
    threat_of_new_entrants = display_force_section(
        "2. Threat of New Entrants", 
        [
            "What are the most significant barriers to entry in this industry (e.g., economies of scale, capital requirements)?",
            "How easy is it for new companies to gain access to distribution channels?",
            "Are there any government regulations or patents that protect the existing players?",
            "How strong is brand loyalty or customer switching costs that might deter new entrants?",
            "What role does technology play in reducing or increasing the threat of new entrants (e.g., new digital platforms or automation)?"
        ], 
        "Rate the threat of new entrants",
        "You rated the Threat of New Entrants as {}. Could there be regulatory, technological, or financial developments that might alter this threat?",
        case_study
    )

    # Bargaining Power of Suppliers
    bargaining_power_of_suppliers = display_force_section(
        "3. Bargaining Power of Suppliers", 
        [
            "How many suppliers are there, and how concentrated is the supplier base?",
            "Can suppliers easily raise their prices or reduce the quality of materials or services they provide?",
            "Are the suppliers offering differentiated products that are critical to the industry?",
            "How easy is it for the company to switch suppliers or find alternative inputs?",
            "Are suppliers vertically integrated (i.e., can they enter the industry as competitors)?"
        ], 
        "Rate the bargaining power of suppliers",
        "You rated the Bargaining Power of Suppliers as {}. How might global supply chain trends or scarcity of materials impact this force?",
        case_study
    )

    # Bargaining Power of Buyers
    bargaining_power_of_buyers = display_force_section(
        "4. Bargaining Power of Buyers", 
        [
            "How price-sensitive are buyers, and what is their willingness to switch to competitors based on price?",
            "How many alternative products or services are available to buyers, and how easy is it for them to switch?",
            "Do buyers have enough purchasing power to influence the terms (e.g., large orders, bulk discounts)?",
            "What role does product differentiation play in keeping buyers from switching to competitors?",
            "Are buyers increasingly focused on sustainability, ethics, or other non-price factors that might influence their purchasing decisions?"
        ], 
        "Rate the bargaining power of buyers",
        "You rated the Bargaining Power of Buyers as {}. Are there recent trends in buyer preferences or purchasing behavior that could influence this rating?",
        case_study
    )

    # Threat of Substitutes
    threat_of_substitutes = display_force_section(
        "5. Threat of Substitutes", 
        [
            "Are there alternative products or services outside the industry that fulfill a similar need for the customer?",
            "How easy is it for customers to switch to substitutes, and what are the associated costs or inconveniences?",
            "Are substitutes improving in quality, performance, or affordability over time?",
            "What is the current trend in customer preferences (e.g., are they moving toward substitute products)?",
            "Are technological advancements creating new substitute products that could disrupt the industry?"
        ], 
        "Rate the threat of substitutes",
        "You rated the Threat of Substitutes as {}. Are there emerging technologies or changing consumer preferences that might affect this force?",
        case_study
    )

    # Display team ratings
    if st.button("Submit Ratings"):
        st.write("### Team's Porter's Five Forces Ratings")
        st.write(f"**1. Competitive Rivalry**: {competitive_rivalry}/10")
        st.write(f"**2. Threat of New Entrants**: {threat_of_new_entrants}/10")
        st.write(f"**3. Bargaining Power of Suppliers**: {bargaining_power_of_suppliers}/10")
        st.write(f"**4. Bargaining Power of Buyers**: {bargaining_power_of_buyers}/10")
        st.write(f"**5. Threat of Substitutes**: {threat_of_substitutes}/10")

        # AI feedback based on overall analysis
        st.write("### AI Chatbot Feedback")
        ai_feedback_prompt = (
            f"The team rated Competitive Rivalry at {competitive_rivalry}, "
            f"Threat of New Entrants at {threat_of_new_entrants}, "
            f"Bargaining Power of Suppliers at {bargaining_power_of_suppliers}, "
            f"Bargaining Power of Buyers at {bargaining_power_of_buyers}, "
            f"and Threat of Substitutes at {threat_of_substitutes}. "
            f"Provide feedback and suggestions for discussion on these forces."
        )

        # Get AI feedback
        response = client.chat.completions.create(model="gpt-4o",  # Or "gpt-4" if you have access
        messages=st.session_state.messages + [{"role": "user", "content": ai_feedback_prompt}])
        chatbot_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": chatbot_reply})
        st.write(f"**Chatbot**: {chatbot_reply.strip()}")

        # Download summary as text
        analysis = f"""
        Porter's Five Forces Analysis for Team {team_name} ({case_study} Case):
        1. Competitive Rivalry: {competitive_rivalry}/10
        2. Threat of New Entrants: {threat_of_new_entrants}/10
        3. Bargaining Power of Suppliers: {bargaining_power_of_suppliers}/10
        4. Bargaining Power of Buyers: {bargaining_power_of_buyers}/10
        5. Threat of Substitutes: {threat_of_substitutes}/10
        """

        st.download_button("Download Analysis as Text", analysis)

