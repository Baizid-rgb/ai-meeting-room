import streamlit as st
import google.generativeai as genai
import os

# Streamlit Page Setup
st.set_page_config(page_title="AI Conference Room", layout="centered")

st.markdown("# 🧠 AI Conference Room (Multi-AI Panel)")
st.markdown("এখানে এআইগুলো নিজেদের মধ্যে ক্রস-চেক করে তোমাকে বেস্ট আউটপুট দেবে।")

# API Configuration (Streamlit Secrets থেকে এপিআই কী নেবে)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key পাওয়া যায়নি! Streamlit Secrets-এ GEMINI_API_KEY যুক্ত করো।")

# User Input
user_input = st.text_area("আলোচনার বিষয় বা প্রম্পট দাও:", placeholder="যেমন: পাইথনের একটি লুপ কোড লেখো বা সেনরো চ্যানেলের আইডিয়া দাও...")

if st.button("START MEETING"):
    if user_input:
        with st.spinner("এআই প্যানেল আলোচনা করছে..."):
            try:
                # AI Model 1: Draft Creator (যেমন জেমিনাই ফ্ল্যাশ)
                model_1 = genai.GenerativeModel('gemini-1.5-flash', system_instruction="তুমি ড্রাফট ক্রিয়েটর। প্রাথমিক সমাধান বা কোড তৈরি করছ।")
                response_1 = model_1.generate_content(user_input)
                
                st.subheader("🤖 AI - 1 (Draft / Code):")
                st.write(response_1.text)
                
                # AI Model 2: Critic & Fixer (রিভিউ এবং বাগ ফিক্সার)
                model_2 = genai.GenerativeModel('gemini-1.5-flash', system_instruction="তুমি ক্রিতিক এবং রিভিউয়ার। আগের এআই-এর দেওয়া কোড বা উত্তরে কোনো ভুল বা বাগ থাকলে তা ধরিয়ে দাও এবং ফাইনাল অপ্টিমাইজড ভার্সন দাও।")
                response_2 = model_2.generate_content(f"আগের আউটপুটটি যাচাই করো এবং ভুল সংশোধন করে বেস্ট রেজাল্ট দাও: {response_1.text}")
                
                st.subheader("⚡ AI - 2 (Critique & Final Optimized Result):")
                st.write(response_2.text)
                
            except Exception as e:
                st.error(f"এরর এসেছে: {e}")
    else:
        st.warning("আগে কিছু একটা লিখে ইনপুট দাও!")