import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="JEE Analyzer App", layout="centered")
st.title("📊 JEE Performance Analyzer with Offline AI")

st.markdown("Upload your performance to visualize growth and get smart AI-like feedback! 💡")

# Load existing scores from CSV or initialize empty DataFrame
CSV_FILE = "jee_scores.csv"
try:
    scores_df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    scores_df = pd.DataFrame(columns=["Date", "Physics", "Chemistry", "Maths", "Total"])

# Input form
with st.form("score_form"):
    st.subheader("Enter New Test Scores")
    date = st.date_input("Test Date", datetime.today())
    physics = st.number_input("Physics Marks", min_value=0, max_value=120, step=1)
    chemistry = st.number_input("Chemistry Marks", min_value=0, max_value=120, step=1)
    maths = st.number_input("Maths Marks", min_value=0, max_value=120, step=1)
    total = physics + chemistry + maths
    submitted = st.form_submit_button("Submit")

    if submitted:
        new_row = {"Date": date, "Physics": physics, "Chemistry": chemistry, "Maths": maths, "Total": total}
        scores_df = pd.concat([scores_df, pd.DataFrame([new_row])], ignore_index=True)
        scores_df.to_csv(CSV_FILE, index=False)
        st.success("Score added and saved locally!")

# Plot if data exists
if not scores_df.empty:
    st.subheader("📈 Performance Over Time")
    scores_df["Date"] = pd.to_datetime(scores_df["Date"])
    scores_df = scores_df.sort_values("Date")
    fig, ax = plt.subplots()
    ax.plot(scores_df["Date"], scores_df["Physics"], label="Physics", marker='o')
    ax.plot(scores_df["Date"], scores_df["Chemistry"], label="Chemistry", marker='o')
    ax.plot(scores_df["Date"], scores_df["Maths"], label="Maths", marker='o')
    ax.plot(scores_df["Date"], scores_df["Total"], label="Total", marker='o', linewidth=2, color='black')
    ax.set_ylabel("Marks")
    ax.set_xlabel("Date")
    ax.set_title("Subject-wise and Total Performance")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.subheader("🧠 AI-style Feedback")
    latest = scores_df.iloc[-1]
    previous = scores_df.iloc[-2] if len(scores_df) > 1 else None

    def suggest_improvement(subject, current, previous):
        if previous is None:
            return f"First attempt in {subject}, keep practicing!"
        if current > previous:
            return f"Good improvement in {subject}, keep up the consistency."
        elif current < previous:
            return f"{subject} score dropped. Review mistakes and revise concepts."
        else:
            return f"{subject} is stable. Try increasing your accuracy."

    for subject in ["Physics", "Chemistry", "Maths"]:
        st.markdown(f"**{subject}:** {suggest_improvement(subject, latest[subject], previous[subject] if previous is not None else None)}")

    st.markdown(f"**Total Marks:** {latest['Total']} — {'Excellent' if latest['Total'] > 300 else 'Needs Improvement' if latest['Total'] < 200 else 'Good job!'}")

else:
    st.warning("No data yet. Please enter your test scores above.")
