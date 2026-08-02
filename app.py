import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Conference Room", layout="centered")

st.markdown("# 🧠 AI Conference Room")
st.markdown("Logical & Real-life Analysis Panel")

groq_key = st.secrets.get("GROQ_API_KEY")

user_input = st.text_area("রিসার্চ টপিক বা প্রম্পট দাও:")

if st.button("RUN ANALYSIS"):
    if user_input:
        if groq_key:
            with st.spinner("অ্যানালিসিস চলছে..."):
                try:
                    client = Groq(api_key=groq_key)
                    
                    # Llama 3.3 (Logical & Real-life Core Analysis)
                    res_1 = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "তুমি একজন ইমোশনলেস, লজিক্যাল এবং রিয়েল-লাইফ সাইকোলজিক্যাল অ্যানালিস্ট। কোনো অপ্রয়োজনীয় কথা বা ফালতু মোটিভেশন না দিয়ে একদম টু-দ্য-পয়েন্ট, লজিক্যাল এবং সংক্ষিপ্ত (Short) রেসপন্স দেবে।"},
                            {"role": "user", "content": user_input}
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    st.subheader("🎯 Result:")
                    st.write(res_1.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"এরর: {e}")
        else:
            st.warning("GROQ_API_KEY পাওয়া যায়নি।")
    else:
        st.warning("আগে কিছু ইনপুট দাও!")
