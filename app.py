import streamlit as st
from openai import OpenAI

st.title("AI Confidence Layer Prototype")
st.write("Test out how an AI distinguishes between verified facts, logical guesses, and speculation.")

# Fetch the key securely from Streamlit Secrets
api_key = st.secrets["GROQ_API_KEY"]

user_question = st.text_input("Ask a question based on your document or topic:")

if st.button("Generate Answer"):
    if not user_question:
        st.warning("Please type a question.")
    else:
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        
        with st.spinner("Analyzing and confidence-scoring response..."):
            prompt = f"""
            Answer the following question: "{user_question}".
            Break your answer down into individual sentences. For each sentence, assign a confidence tag:
            - [GROUNDED] if it is a hard fact.
            - [INFERRED] if it is a logical deduction.
            - [SPECULATIVE] if it is a guess or creative generation.
            
            Format your output clearly sentence by sentence with its tag.
            """
            
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            
            answer_text = response.choices[0].message.content
            
            st.subheader("Confidence-Layered Output:")
            for line in answer_text.split('\n'):
                if "[GROUNDED]" in line:
                    st.markdown(f'<p style="background-color: #d4edda; padding: 8px; border-radius: 5px;">🟢 {line}</p>', unsafe_allow_html=True)
                elif "[INFERRED]" in line:
                    st.markdown(f'<p style="background-color: #fff3cd; padding: 8px; border-radius: 5px;">🟡 {line}</p>', unsafe_allow_html=True)
                elif "[SPECULATIVE]" in line:
                    st.markdown(f'<p style="background-color: #f8d7da; padding: 8px; border-radius: 5px;">🔴 {line}</p>', unsafe_allow_html=True)
                else:
                    st.write(line)
