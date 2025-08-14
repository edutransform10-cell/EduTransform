# app.py
import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="EduTransform", page_icon="📘", layout="wide")

# --- Branding ---
st.image("logo.png", width=120)  # logo.png (your EduTransform logo)
st.title("EduTransform")
st.subheader("Student Empowerment Platform")

st.markdown("---")

# --- Role Selection ---
role = st.sidebar.selectbox("Login as:", ["Student", "Parent", "Teacher"])

# --- Data Setup ---
MOOD_FILE = "mood_log.csv"
LEADERBOARD_FILE = "leaderboard.csv"
BOOKINGS_FILE = "bookings.csv"

def load_csv(file, cols):
    if not os.path.exists(file):
        return pd.DataFrame(columns=cols)
    return pd.read_csv(file)

# -- STUDENT DASHBOARD --
if role == "Student":
    st.header("Student Dashboard")
    col1, col2 = st.columns(2)

    # Mood & Focus Tracker
    with col1:
        today = datetime.date.today()
        st.subheader("Track Your Mood & Focus")
        mood = st.selectbox("Today's mood", ["Happy", "Sad", "Angry", "Neutral"])
        focus = st.select_slider("Focus Level (1 = Distracted, 5 = Highly Focused)", options=[1,2,3,4,5])
        if st.button("Log Mood & Focus"):
            df = load_csv(MOOD_FILE, ["Date","Mood","Focus"])
            df = df.append({"Date": today, "Mood": mood, "Focus": focus}, ignore_index=True)
            df.to_csv(MOOD_FILE, index=False)
            st.success("Entry logged!")
    with col2:
        df = load_csv(MOOD_FILE, ["Date","Mood","Focus"])
        if not df.empty:
            st.write("Mood Trends")
            st.bar_chart(df["Mood"].value_counts())
            st.write("Focus Trends")
            st.line_chart(df.set_index("Date")["Focus"])
        else:
            st.info("No mood/focus data yet.")

    st.markdown("---")
    # Leaderboard
    st.subheader("Leaderboard")
    df_leaderboard = load_csv(LEADERBOARD_FILE, ["Student", "Points"])
    st.write(df_leaderboard.sort_values("Points", ascending=False).reset_index(drop=True))
    if st.button("Add Points"):
        name = st.text_input("Your Name:", key="student_leaderboard_name")
        points = st.number_input("Points to Add", min_value=1, step=1, key="student_leaderboard_points")
        if name:
            df_leaderboard = df_leaderboard.append({"Student": name, "Points": points}, ignore_index=True)
            df_leaderboard.to_csv(LEADERBOARD_FILE, index=False)
            st.success("Points added!")
    st.markdown("---")

    # Booking System
    st.subheader("Book Psychologist Session")
    name = st.text_input("Student Name", key="student_booking_name")
    date = st.date_input("Select date")
    reason = st.selectbox("Reason", ["Stress", "Anxiety", "Career Guidance", "Other"])
    if st.button("Book Session"):
        df_book = load_csv(BOOKINGS_FILE, ["Name","Date","Reason"])
        df_book = df_book.append({"Name": name, "Date": date, "Reason": reason}, ignore_index=True)
        df_book.to_csv(BOOKINGS_FILE, index=False)
        st.success("Session booked!")

# -- PARENT DASHBOARD --
elif role == "Parent":
    st.header("Parent Dashboard")
    st.subheader("Book Psychologist for Your Child")
    name = st.text_input("Parent Name", key="parent_booking_name")
    child = st.text_input("Child Name")
    date = st.date_input("Date")
    reason = st.selectbox("Reason", ["Stress", "Academic", "Family", "Other"])
    if st.button("Book Session (Parent)"):
        df_book = load_csv(BOOKINGS_FILE, ["Name","Child","Date","Reason"])
        df_book = df_book.append({"Name": name, "Child": child, "Date": date, "Reason": reason}, ignore_index=True)
        df_book.to_csv(BOOKINGS_FILE, index=False)
        st.success("Session booked!")
    st.markdown("---")
    st.subheader("Check Leaderboard")
    df_leaderboard = load_csv(LEADERBOARD_FILE, ["Student", "Points"])
    st.write(df_leaderboard.sort_values("Points", ascending=False).reset_index(drop=True))

# -- TEACHER DASHBOARD --
elif role == "Teacher":
    st.header("Teacher Dashboard")
    st.subheader("Student Mood/Focus Analytics")
    df = load_csv(MOOD_FILE, ["Date","Mood","Focus"])
    if not df.empty:
        mood_stats = df["Mood"].value_counts()
        st.write("Mood Distribution")
        st.bar_chart(mood_stats)
        st.write("Average Focus Score:", df["Focus"].mean())
        st.line_chart(df.set_index("Date")["Focus"])
        st.write(df)
    else:
        st.info("No student mood/focus data yet.")

    st.markdown("---")
    st.subheader("Leaderboard Overview")
    df_leaderboard = load_csv(LEADERBOARD_FILE, ["Student", "Points"])
    st.write(df_leaderboard.sort_values("Points", ascending=False).reset_index(drop=True))

    st.markdown("---")
    st.subheader("Session Bookings")
    df_book = load_csv(BOOKINGS_FILE, ["Name","Child","Date","Reason"])
    st.write(df_book if not df_book.empty else "No bookings yet.")

# -- Footer/Info --
st.markdown("---")
st.info("© EduTransform | Student Empowerment Platform")

