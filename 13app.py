import streamlit as st
import pandas as pd
from io import BytesIO

# Load data
df = pd.read_csv("student13.csv")

st.title("📊 EduTrack Dashboard")
st.caption("Track. Analyze. Improve.")
st.dataframe(df)

# Charts
st.subheader("📈 Marks Comparison")
st.bar_chart(df.set_index("Name")["Marks"])

st.subheader("📉 Attendance Trend")
st.line_chart(df.set_index("Name")["Attendance"])

# Select student
student = st.selectbox("Choose a student:", df["Name"], key="student_select")
attendance = int(df.loc[df["Name"]==student, "Attendance"].values[0])
marks = int(df.loc[df["Name"]==student, "Marks"].values[0])

st.metric(label="Attendance %", value=attendance)
st.metric(label="Marks", value=marks)

# Alert
if attendance < 75:
    st.error(f"{student} has low attendance ({attendance}%) ❌")
else:
    st.success(f"{student}'s attendance is good ({attendance}%) ✅")

# Update form
with st.form("update_form"):
    st.subheader("✏️ Update Student Data")
    new_attendance = st.number_input("Update Attendance %", min_value=0, max_value=100, value=attendance, key="attendance_input")
    new_marks = st.number_input("Update Marks", min_value=0, max_value=100, value=marks, key="marks_input")
    submitted = st.form_submit_button("Save Changes")

    if submitted:
        df.loc[df["Name"]==student, "Attendance"] = new_attendance
        df.loc[df["Name"]==student, "Marks"] = new_marks
        df.to_csv("student13.csv", index=False)
        st.success(f"✅ Updated {student}'s record successfully!")

# Add new student form
with st.form("add_student_form"):
    st.subheader("➕ Add New Student")
    new_name = st.text_input("Student Name", key="new_name")
    new_attendance = st.number_input("Attendance %", min_value=0, max_value=100, key="new_attendance")
    new_marks = st.number_input("Marks", min_value=0, max_value=100, key="new_marks")
    add = st.form_submit_button("Add Student")

    if add:
        if new_name.strip() != "":
            new_row = {"Name": new_name, "Attendance": new_attendance, "Marks": new_marks}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv("student13.csv", index=False)
            st.success(f"✅ Added {new_name} successfully!")
        else:
            st.error("❌ Please enter a valid student name.")

# Delete student form
with st.form("delete_student_form"):
    st.subheader("🗑️ Delete Student")
    del_name = st.selectbox("Select student to delete:", df["Name"], key="delete_select")
    delete = st.form_submit_button("Delete Student")

    if delete:
        df = df[df["Name"] != del_name]
        df.to_csv("student13.csv", index=False)
        st.success(f"✅ Deleted {del_name} successfully!")

# Export options
st.subheader("📥 Export Updated Data")

# CSV export
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download as CSV",
    data=csv,
    file_name="updated_students.csv",
    mime="text/csv"
)

# Excel export
output = BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, sheet_name="Students")
    worksheet = writer.sheets["Students"]
    worksheet.set_column("A:C", 20)  # widen columns
excel_data = output.getvalue()

st.download_button(
    label="Download as Excel",
    data=excel_data,
    file_name="updated_students.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
