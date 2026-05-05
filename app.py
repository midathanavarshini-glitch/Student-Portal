import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Portal", layout="wide")

# ---------------- LOGIN ----------------
def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
        else:
            st.error("Wrong credentials")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ---------------- MAIN ----------------
st.title("🎓 Student Result Portal")

uploaded_files = st.file_uploader(
    "Upload Excel Files", type=["xlsx"], accept_multiple_files=True
)

if uploaded_files:
    all_data = []

    for file in uploaded_files:
        df = pd.read_excel(file)

        # Clean column names
        df.columns = df.columns.str.strip()

        df["Source"] = file.name
        all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)

    st.success("Files uploaded successfully!")

    # ---------------- STUDENT LIST ----------------
    students = combined_df[["Hallticket Number", "Student Name"]].drop_duplicates()

    selected = st.sidebar.selectbox(
        "Select Student",
        students["Hallticket Number"]
    )

    student_data = combined_df[
        combined_df["Hallticket Number"] == selected
    ]

    if not student_data.empty:
        st.subheader("👤 Student Details")

        first = student_data.iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {first['Student Name']}")
            st.write(f"**Hall Ticket:** {first['Hallticket Number']}")

        # ---------------- TABLE ----------------
        st.subheader("📊 Academic Records")
        st.dataframe(student_data, use_container_width=True)

        # ---------------- GRAPH ----------------
        st.subheader("📈 Performance Graph")

        if "External Marks" in student_data.columns:
            chart = student_data[["Course Name", "External Marks"]]
            chart = chart.set_index("Course Name")

            st.bar_chart(chart)

        # ---------------- DOWNLOAD ----------------
        csv = student_data.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Report", csv, "student_report.csv")