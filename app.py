import streamlit as st
from google import genai
from groq import Groq

st.set_page_config(page_title="AI Conference Room", layout="centered")

st.markdown("# 🧠 AI Conference Room (Multi-AI Panel)")
st.markdown("এখানে জেমিনাই এবং গ্রক একসাথে কাজ করে তোমাকে সেরা আউটপুট দেবে।")

gemini_key = st.secrets.get("GEMINI_API_KEY")
groq_key = st.secrets.get("GROQ_API_KEY")

user_input = st.text_area("আলোচনার বিষয় বা প্রম্পট দাও:", placeholder="যেমন: সেনরো চ্যানেলের জন্য ভিডিওর স্ক্রিপ্ট বা আইডিয়া...")

if st.button("START MEETING"):
    if user_input:
        with st.spinner("এআই প্যানেল আলোচনা করছে..."):
            try:
                # AI 1: Gemini (Draft Creator) - লেটেস্ট জেমিনাই মডেল ব্যবহার করা হয়েছে
                if gemini_key:
                    client_gemini = genai.Client(api_key=gemini_key)
                    response_1 = client_gemini.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_input,
                    )
                    st.subheader("🤖 AI - 1 (Gemini Draft):")
                    st.write(response_1.text)
                else:
                    st.error("GEMINI_API_KEY পাওয়া যায়নি!")
                
                # AI 2: Groq (Llama Model - Critic & Fixer)
                if groq_key and gemini_key:
                    client_groq = Groq(api_key=groq_key)
                    chat_completion = client_groq.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": "তুমি ক্রিতিক এবং রিভিউয়ার। আগের এআই-এর দেওয়া কন্টেন্টে কোনো ভুল বা দুর্বলতা থাকলে তা শুধরে ফাইনাল অপ্টিমাইজড ভার্সন দাও।"
                            },
                            {
                                "role": "user",
                                "content": f"মূল প্রম্পট: {user_input}\n\nপ্রথম এআই এর আউটপুট: {response_1.text}"
                            }
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    st.subheader("⚡ AI - 2 (Groq Llama - Final Optimized Result):")
                    st.write(chat_completion.choices[0].message.content)
                else:
                    st.warning("GROQ_API_KEY যোগ করা হয়নি, তাই দ্বিতীয় এআই কাজ করছে না।")
                
            except Exception as e:
                st.error(f"এরর এসেছে: {e}")
    else:
        st.warning("আগে কিছু লিখে ইনপুট দাও!")
