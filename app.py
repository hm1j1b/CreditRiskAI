import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Load the API Key
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ API Key not found! Please check your .env file.")
    st.stop()

# 2. Load the Financial Data (CSV)
@st.cache_data
def load_data():
    return pd.read_csv("customer_database.csv")

df = load_data()

# 3. AI Behavioural Risk Analysis Function
def analyze_behavioral_risk(essay_text, credit_score, transactions_history):
    llm = ChatOpenAI(model="gpt-5.1", temperature=0)
    
    # We give the AI the credit score as context so it knows if the user is lying
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Senior Credit Risk Officer. Analyze the loan application essay."),
        ("human", """
        Applicant Credit Score: {score}
        Recent Transactions: "{transactions}"
        Applicant Essay: "{text}"
        
        Task:
        1. Does the essay tone match the credit score? (e.g. Low score but claims 'perfect financial health' = Suspicious).
        2. Look for keywords like 'gambling', 'crypto', 'urgent', 'pay off debts'.
        3. Give a Behavioral Risk Score from 0 (Safe) to 100 (Dangerous).
        4. Explain your reasoning in one sentence.
        5. COMPLIANCE CHECK: Ensure your decision is NOT based on the applicant's name, gender, or location.
        6. State explicitly: "Bias Check: Passed" if the reasoning is purely financial/behavioral.
        
        Output Format:
        Score: [Number]
        Reason: [Text]
        """)
    ])
    
    chain = prompt | llm
    response = chain.invoke({"score": credit_score, "text": essay_text, "transactions": transactions_history})
    return response.content

# --- THE USER INTERFACE (Streamlit) ---
st.set_page_config(page_title="AI Credit Scorer", layout="wide")

st.title("Multimodal Credit Risk AI Assessment")
st.markdown("Combines **Structured Data (CSV)** + **Unstructured Data (Text)**.")

# Split screen into two columns
col1, col2 = st.columns([1, 2])

with col1:
    st.header("1. Select Customer")
    # Dropdown to pick a person from our CSV
    selected_name = st.selectbox("Choose an applicant:", df['Name'])
    
    # Retrieve their financial stats automatically
    customer_data = df[df['Name'] == selected_name].iloc[0]
    
    st.info(f"📊 **Financial Profile for {selected_name}**")
    st.write(f"**Income:** ${customer_data['Income']:,}")
    st.write(f"**Debt:** ${customer_data['Debt']:,}")
    st.write(f"**Credit Score:** {customer_data['Credit_Score']}")
    st.write("---")
    st.write("**Recent Transactions:**")
    st.code(customer_data['Recent_Transactions'])
    
    # Simple Math Rule for "Hard Risk"
    hard_risk_score = 100 - (customer_data['Credit_Score'] / 8.5)
    st.metric("Financial Risk", f"{hard_risk_score:.1f}/100")

with col2:
    st.header("2. Behavioral Analysis (AI)")
    
    default_essay = "I have a stable job and I need this loan to renovate my kitchen. I have always paid my bills on time."
    essay_input = st.text_area("Applicant's Statement / Loan Essay:", default_essay, height=150)
    
    if st.button("Run Multimodal Assessment"):
        with st.spinner("AI is reading the essay, transactions, and cross-referencing with CSV data..."):
            
            # CALL THE AI
            ai_result = analyze_behavioral_risk(
                essay_input, 
                customer_data['Credit_Score'], 
                customer_data['Recent_Transactions']
            )
            
            # Parse the result (Simple string splitting)
            try:
                score_text = ai_result.split("Score:")[1].split("\n")[0].strip()
                soft_risk_score = float(score_text)
                reasoning = ai_result.split("Reason:")[1].strip()
            except:
                # Fallback if AI output format varies
                soft_risk_score = 50 
                reasoning = ai_result

            # Final Score = 60% Math + 40% AI
            final_score = (hard_risk_score * 0.6) + (soft_risk_score * 0.4)
            
            # Display Results
            st.success("Analysis Complete!")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Financial Risk", f"{hard_risk_score:.0f}")
            m2.metric("Behavioral Risk (AI)", f"{soft_risk_score:.0f}")
            m3.metric("🏆 FUSION SCORE", f"{final_score:.0f}")
            
            st.subheader("🤖 AI Reasoning:")
            st.warning(reasoning)
            
            if final_score > 60:
                st.error("Recommendation: REJECT LOAN")
            else:
                st.success("Recommendation: APPROVE LOAN")