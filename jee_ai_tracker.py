import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

st.set_page_config(page_title="JEE AI Tracker", layout="centered")
st.title("📊 JEE Performance Analyzer (Offline AI)")

# File to store data
CSV_FILE = "jee_scores.csv"

# Get user input
st.subheader("🔢 Enter Your Marks")
date = st.date_input("Test Date", value=datetime.today())
physics = st.number_input("Physics Marks", min_value=0, max_value=100, step=1)
chemistry = st.number_input("Chemistry Marks", min_value=0, max_value=100, step=1)
maths = st.number_input("Maths Marks", min_value=0, max_value=100, step=1)

if st.button("💾 Save & Analyze"):
    # Save data
    new_data = pd.DataFrame([{
        "Date": date,
        "Physics": physics,
        "Chemistry": chemistry,
        "Maths": maths
    }])

    if os.path.exists(CSV_FILE):
        old_data = pd.read_csv(CSV_FILE)
        data = pd.concat([old_data, new_data], ignore_index=True)
    else:
        data = new_data

    data.to_csv(CSV_FILE, index=False)
    st.success("✅ Saved successfully!")

    st.subheader("📁 Your Performance History")
    st.dataframe(data)

    # Graph
    st.subheader("📈 Progress Over Time")
    fig, ax = plt.subplots()
    data['Date'] = pd.to_datetime(data['Date'])
    ax.plot(data['Date'], data['Physics'], label="Physics", marker="o")
    ax.plot(data['Date'], data['Chemistry'], label="Chemistry", marker="o")
    ax.plot(data['Date'], data['Maths'], label="Maths", marker="o")
    ax.set_ylabel("Marks")
    ax.set_xlabel("Test Date")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # AI Feedback (offline)
    st.subheader("🧠 Smart AI Feedback")
    recent = data.iloc[-3:] if len(data) >= 3 else data

    for subject in ['Physics', 'Chemistry', 'Maths']:
        avg = recent[subject].mean()
        trend = recent[subject].diff().mean()
        feedback = f"📘 {subject}: Avg = {avg:.1f}, Trend = {'⬆️ Improving' if trend > 0 else '⬇️ Dropping' if trend < 0 else '➖ Stable'}"
        if avg < 50:
            feedback += " (⚠️ Needs attention)"
        elif avg > 85:
            feedback += " (🔥 Excellent!)"
        st.write(feedback)

else:
    if os.path.exists(CSV_FILE):
        st.info("📂 You have saved data. Click 'Save & Analyze' to refresh graph.")
    else:
        st.info("🚀 Start by entering your first test marks.")

