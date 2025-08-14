import streamlit as st

st.set_page_config(page_title="EduTransform", page_icon="📘")
st.title("EduTransform")
st.subheader("Student Empowerment Platform")

st.write("Welcome to EduTransform! Collaborate as Student, Parent, or Teacher.")

role = st.sidebar.selectbox("Login as", ["Student", "Parent", "Teacher"])
st.write(f"You are viewing the {role} dashboard.")
