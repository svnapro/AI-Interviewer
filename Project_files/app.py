import streamlit as st
from core.llm import chat_with_ai

st.set_page_config(page_title="AI Interviewer (ChatGPT Free)", page_icon="💼", layout="centered")

st.title("💼 AI Interviewer (ChatGPT Free via OpenRouter)")
st.caption("Simulate interviews using GPT-like models, completely free.")

# ---- Session state ----
if "started" not in st.session_state:
    st.session_state.started = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

# ---- Sidebar ----
st.sidebar.header("🎯 Interview Setup")
round_type = st.sidebar.selectbox("Select Interview Round", ["HR", "Technical", "Managerial", "System Design"])
tech = st.sidebar.selectbox("Select Technology", ["Python", "Java", "Web Development", "Machine Learning", "Cloud", "SQL"])

# ---- Start Interview ----
if not st.session_state.started:
    st.info("Select interview type and click below to start.")
    if st.button("🚀 Start Interview"):
        st.session_state.started = True
        system_prompt = {
            "role": "system",
            "content": f"You are a professional {round_type} interviewer for a {tech} position. "
                       f"Start with 'Tell me about yourself' and then continue asking one question at a time "
                       f"based on the candidate's answers. Keep the tone realistic and conversational."
        }
        with st.spinner("Preparing interviewer..."):
            reply = chat_with_ai([system_prompt, {"role": "user", "content": "Start the interview."}])
        st.session_state.messages = [{"role": "assistant", "content": reply}]
        st.rerun()

else:
    st.subheader(f"🧠 {round_type} Interview — {tech}")
    for msg in st.session_state.messages:
        who = "🧍 You" if msg["role"] == "user" else "🤖 Interviewer"
        st.markdown(f"**{who}:** {msg['content']}")

    if not st.session_state.feedback_given:
        ans = st.text_input("Your Answer:", key="answer")

        c1, c2, c3 = st.columns([1,1,1])

        if c1.button("Send") and ans.strip():
            st.session_state.messages.append({"role": "user", "content": ans})
            with st.spinner("Interviewer is thinking..."):
                messages = [{"role": "system",
                             "content": f"You are a {round_type} interviewer for a {tech} job. "
                                        "Ask realistic follow-up questions based on conversation."}] + st.session_state.messages
                reply = chat_with_ai(messages)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

        if c2.button("🛑 End Interview"):
            with st.spinner("Generating feedback..."):
                transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                feedback_prompt = (
                    f"You are an expert interviewer evaluating this {round_type} interview for a {tech} position. "
                    f"Provide feedback including strengths, areas to improve, and a score out of 10.\n\nTranscript:\n{transcript}"
                )
                reply = chat_with_ai([
                    {"role": "system", "content": "You are an expert HR evaluator."},
                    {"role": "user", "content": feedback_prompt}
                ])
            st.session_state.messages.append({"role": "assistant", "content": f"📋 **Feedback:**\n\n{reply}"})
            st.session_state.feedback_given = True
            st.rerun()

        if c3.button("🔁 Restart"):
            st.session_state.clear()
            st.rerun()
    else:
        st.success("✅ Interview complete. Review your feedback above.")
        if st.button("🔁 New Interview"):
            st.session_state.clear()
            st.rerun()
