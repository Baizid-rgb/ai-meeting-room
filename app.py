import streamlit as st
from google import genai
from groq import Groq

st.set_page_config(page_title="AI Conference Room", layout="centered")

st.markdown("# 🧠 AI Conference Room (Multi-AI Panel)")
st.markdown("এখানে জেমিনাই এবং গ্রক একসাথে কাজ করে তোমাকে আউটপুট দেবে।")

gemini_key = st.secrets.get("GEMINI_API_KEY")
groq_key = st.secrets.get("GROQ_API_KEY")

user_input = st.text_area("আলোচনার বিষয় বা প্রম্পট দাও:", placeholder="যেমন: সেনরো চ্যানেলের জন্য ভিডিওর স্ক্রিপ্ট বা আইডিয়া...")

if st.button("START MEETING"):
    if user_input:
        with st.spinner("এআই প্যানেল আলোচনা করছে..."):
            try:
                # 1. Gemini
                if gemini_key:
                    try:
                        client_gemini = genai.Client(api_key=gemini_key)
                        response_1 = client_gemini.models.generate_content(
                            model='gemini-2.0-flash',
                            contents=user_input,
                        )
                        st.subheader("🤖 Gemini Draft:")
                        st.write(response_1.text)
                    except Exception as g_err:
                        st.warning(f"Gemini লিমি트 শেষ বা কোটা পূর্ণ: {g_err}")
                
                # 2. Groq (Llama 3.3 - শক্তিশালী এবং ফ্রি)
                if groq_key:
                    client_groq = Groq(api_key=groq_key)
                    chat_groq = client_groq.chat.completions.create(
                        messages=[{"role": "user", "content": user_input}],
                        model="llama-3.3-70b-versatile",
                    )
                    st.subheader("⚡ Groq Llama Result:")
                    st.write(chat_groq.choices[0].message.content)
                else:
                    st.warning("GROQ_API_KEY পাওয়া যায়নি।")
                
            except Exception as e:
                st.error(f"এরর এসেছে: {e}")
    else:
        st.warning("আগে কিছু লিখে ইনপুট দাও!")
