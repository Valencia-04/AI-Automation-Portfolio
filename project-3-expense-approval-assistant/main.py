import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Expense Approval Automation", page_icon="💼")

st.title("💼 Expense Approval Automation Tool")
st.write("Upload your expense Excel file and get approvals instantly.")

# Upload file
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
    else:
        # Check columns
        required_cols = {"Employee", "Department", "Amount", "Reason"}
        if not required_cols.issubset(df.columns):
            st.error(f"Missing columns. Found: {df.columns.tolist()}")
        else:
            # Apply rules
            def approval_rule(amount):
                if amount <= 200:
                    return "Approved"
                elif amount <= 500:
                    return "Pending Manager Approval"
                else:
                    return "Rejected"

            df["Status"] = df["Amount"].apply(approval_rule)

            # Show summary
            st.subheader("✅ Summary")
            total = len(df)
            approved = (df["Status"] == "Approved").sum()
            pending = (df["Status"] == "Pending Manager Approval").sum()
            rejected = (df["Status"] == "Rejected").sum()
            st.write(f"Total Expenses: {total}")
            st.write(f"Approved: {approved}")
            st.write(f"Pending Manager Approval: {pending}")
            st.write(f"Rejected: {rejected}")

            # Show detailed table
            st.subheader("📋 Detailed View")
            st.dataframe(df)

            # Download processed file
            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            st.download_button(
                label="📥 Download Processed Expenses",
                data=towrite,
                file_name="processed_expenses.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
