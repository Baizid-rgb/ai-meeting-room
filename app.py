import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Conference Room", layout="centered")

st.markdown("# 🧠 AI Conference Room (Multi-AI Team)")
st.markdown("এখানে গ্রকের তিনটি ভিন্ন শক্তিশালী এআই টিম একসাথে কাজ করছে।")

groq_key = st.secrets.get("GROQ_API_KEY")

user_input = st.text_area("আলোচনার বিষয় বা প্রম্পট দাও:", placeholder="যেমন: সেনরো চ্যানেলের জন্য ভিডিওর স্ক্রিপ্ট বা আইডিয়া...")

if st.button("START MEETING"):
    if user_input:
        if groq_key:
            with st.spinner("এআই টিম আলোচনা করছে..."):
                try:
                    client = Groq(api_key=groq_key)
                    
                    # 1. Llama 3.3 (ডাফট বা মূল আইডিয়া তৈরি করবে)
                    res_1 = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "তুমি প্রধান কন্টেন্ট ক্রিয়েটর। ব্যবহারকারীর প্রম্পট অনুযায়ী চমৎকার প্রাথমিক ড্রাফট বা আইডিয়া তৈরি করো।"},
                            {"role": "user", "content": user_input}
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    st.subheader("🤖 AI - 1 (Llama 3.3 Draft):")
                    st.write(res_1.choices[0].message.content)
                    
                    # 2. Mixtral (লজিক এবং গভীরতা যাচাই করবে)
                    res_2 = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "তুমি লজিক অ্যানালিস্ট। প্রথম এআই-এর কন্টেন্ট বিশ্লেষণ করে আরও গভীরে তথ্য এবং বাস্তবসম্মত পয়েন্ট যোগ করো।"},
                            {"role": "user", "content": f"মূল প্রম্পট: {user_input}\n\nপ্রথম এআই এর আউটপুট: {res_1.choices[0].message.content}"}
                        ],
                        model="mixtral-8x7b-32768",
                    )
                    st.subheader("⚡ AI - 2 (Mixtral Deep Analysis):")
                    st.write(res_2.choices[0].message.content)

                    # 3. Gemma 2 (ফাইনাল রিভিউ ও অপ্টিমাইজড রূপ দেবে)
                    res_3 = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "তুমি চিফ এডিটর ও রিভিউয়ার। আগের দুই এআই-এর তথ্য মিলিয়ে একদম নিখুঁত, আকর্ষণীয় এবং ফাইনাল আউটপুট উপস্থাপন করো।"},
                            {"role": "user", "content": f"মূল প্রম্পট: {user_input}\n\nএআই ১: {res_1.choices[0].message.content}\n\nএআই ২: {res_2.choices[0].message.content}"}
                        ],
                        model="gemma2-9b-it",
                    )
                    st.subheader("🎯 AI - 3 (Gemma 2 Final Optimized Result):")
                    st.write(res_3.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"এরর এসেছে: {e}")
        else:
            st.warning("GROQ_API_KEY পাওয়া যায়নি।")
    else:
        st.warning("আগে কিছু লিখে ইনপুট দাও!")
