import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
from datetime import datetime
import os

# 👇 Voice input function
from utils.voice_input import get_voice_input

# ✅ Load Gemini API key securely
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ App UI
st.set_page_config(page_title="Nyay.AI – Your Legal Friend", layout="centered")
st.title("⚖️ Nyay.AI – Your Voice-based Legal Friend 🇮🇳")

# ✅ Sidebar Feature Select
feature = st.sidebar.radio("Choose Feature", ["💬 Legal Advice", "📝 Draft RTI", "🚔 File FIR"])

# ✅ Load the appropriate prompt template
if feature == "💬 Legal Advice":
    with open("prompts/legal_prompts.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()
elif feature == "📝 Draft RTI":
    with open("prompts/rti_prompt.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()
elif feature == "🚔 File FIR":
    with open("prompts/fir_prompt.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()

# ✅ Voice/Text input mode
input_method = st.radio("Choose Input Mode", ["📝 Type your question", "🎤 Use voice input"])
user_question = ""

if input_method == "📝 Type your question":
    user_question = st.text_area("Enter your legal question:")
else:
    if st.button("🎤 Record Voice"):
        with st.spinner("🎙️ Listening... Please speak your question"):
            user_question = get_voice_input()
        st.success("✅ Voice captured successfully!")
        st.write("You asked:", user_question)
        st.session_state["generate"] = True  # Automatically trigger

# ✅ Generate Response
if st.button("⚡ Generate") or st.session_state.get("generate"):
    if user_question.strip():
        full_prompt = prompt_template.replace("{{QUESTION}}", user_question)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        try:
            response = model.generate_content(full_prompt)
            ai_response = response.text

            # ✅ Feature title
            if feature == "📝 Draft RTI":
                st.subheader("✅ Drafted RTI Application:")
            elif feature == "🚔 File FIR":
                st.subheader("🚨 Draft FIR Report:")
            else:
                st.subheader("🧠 Nyay.AI Response:")

            # ✅ Show response
            st.markdown(ai_response)

            # ✅ Speak the answer aloud
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                engine.say(ai_response)
                engine.runAndWait()
            except Exception as e:
                st.warning("🔈 Couldn't read out loud (TTS not supported on this system)")

            # ✅ Prepare & offer PDF
            file_name = f"nyay_ai_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"User Query: {user_question}\n\nResponse:\n{ai_response}")
            pdf.output(file_name)

            with open(file_name, "rb") as f:
                st.download_button("📄 Download as PDF", f, file_name)
            os.remove(file_name)

        except Exception as e:
            st.error("⚠️ Error! Daily limit or request issue. Try again later.")
            st.text(f"Debug info: {str(e)}")
    else:
        st.warning("❗ Please enter or record a question before generating a response.")

