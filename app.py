import streamlit as st
import openai
import os
from dotenv import load_dotenv
import time

load_dotenv()
openai.api_key = st.secrets["openai"]["OPENAI_API_KEY"]

st.title("🤖 Ask 3 AIs")
st.write("Compare speed, cost, and quality!")

question = st.text_input("Your question:", placeholder="Explain quantum computing")

# Cost per 1K tokens (approximate)
COSTS = {
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-4o": {"input": 0.005, "output": 0.015}
}

def calculate_cost(model, input_tokens, output_tokens):
    input_cost = (input_tokens / 1000) * COSTS[model]["input"]
    output_cost = (output_tokens / 1000) * COSTS[model]["output"]
    return input_cost + output_cost

if st.button("Ask All AIs"):
    if question:
        models = ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"]
        cols = st.columns(3)
        
        for i, model in enumerate(models):
            with cols[i]:
                st.subheader(f"{model}")
                
                start = time.time()
                
                try:
                    response = openai.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": question}],
                        max_tokens=150
                    )
                    
                    elapsed = time.time() - start
                    answer = response.choices[0].message.content
                    
                    # Get token usage
                    usage = response.usage
                    cost = calculate_cost(model, usage.prompt_tokens, usage.completion_tokens)
                    
                    # Display metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("⏱️ Time", f"{elapsed:.2f}s")
                    with col2:
                        st.metric("💰 Cost", f"${cost:.4f}")
                    
                    # Display answer
                    st.write("**Answer:**")
                    st.write(answer)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a question!")