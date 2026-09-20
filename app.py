import streamlit as st
from agent import optimize_prompt, execute_prompt_with_metrics, mask_pii

st.set_page_config(page_title="Prompt Optimizer & Executor", layout="wide")

st.title("⚡ Prompt Optimizer & Executor")
st.write("Automatically mask PII, engineer high-performing prompts, and track execution metrics.")

raw_prompt = st.text_area("Enter your raw query:", height=100)

if st.button("Sanitize & Optimize", type="primary"):
    if raw_prompt.strip():
        with st.spinner("Running Presidio PII Masking and Prompt Engineering..."):
            st.session_state.pop('raw_out', None)
            st.session_state.pop('opt_out', None)
            
            safe_prompt = mask_pii(raw_prompt)
            st.session_state['safe_prompt'] = safe_prompt
            
            result = optimize_prompt(safe_prompt)
            st.session_state['result'] = result
    else:
        st.warning("Please enter a prompt first.")

# Display optimization breakdown
if 'result' in st.session_state:
    result = st.session_state['result']
    safe_prompt = st.session_state['safe_prompt']
    
    st.markdown("---")
    st.subheader("🔒 PII Sanitization Check")
    st.info(f"**Cleaned Input:** {safe_prompt}")

    col_a, col_b = st.columns(2)
    with col_a:
        st.success(f"**Assigned Persona:** {result.persona_used}")
    with col_b:
        st.success(f"**Reasoning:** {result.reasoning}")

    st.subheader("📝 Optimized Prompt")
    st.code(result.improved_prompt, language="text")
    st.markdown("---")

    if st.button("🚀 Run & Compare Execution"):
        with st.spinner("Executing both prompts via Groq..."):
            raw_out, raw_time, raw_tokens = execute_prompt_with_metrics(safe_prompt)
            opt_out, opt_time, opt_tokens = execute_prompt_with_metrics(result.improved_prompt)

        st.session_state['raw_out'] = raw_out
        st.session_state['raw_time'] = raw_time
        st.session_state['raw_tokens'] = raw_tokens
        st.session_state['opt_out'] = opt_out
        st.session_state['opt_time'] = opt_time
        st.session_state['opt_tokens'] = opt_tokens

# Display side-by-side results cleanly
if 'raw_out' in st.session_state:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔴 Basic Prompt Execution")
        st.metric(label="Latency", value=f"{st.session_state['raw_time']} ms")
        st.metric(label="Total Tokens Used", value=st.session_state['raw_tokens'])
        st.markdown(st.session_state['raw_out'])
        
    with col2:
        st.subheader("🟢 Optimized Prompt Execution")
        st.metric(label="Latency", value=f"{st.session_state['opt_time']} ms")
        st.metric(label="Total Tokens Used", value=st.session_state['opt_tokens'])
        st.markdown(st.session_state['opt_out'])