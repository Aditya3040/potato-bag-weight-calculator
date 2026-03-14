import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
from datetime import date

st.set_page_config(page_title="Potato Bag Weight Calculator", layout="wide")

# ---------------- HEADER ----------------

if os.path.exists("logo.png"):
    st.image("logo.png", width=200)

st.markdown("## SOHAM TRADERS")
st.markdown("Mob - 9763916101 / 9021653848")
st.markdown("PepsiCo India Holdings Pvt Ltd")

st.divider()

# ---------------- FARMER INFO ----------------

st.subheader("Farmer Information")

c1,c2,c3 = st.columns(3)

with c1:
    farmer = st.text_input("Farmer Name")

with c2:
    farmer_id = st.text_input("Farmer ID")

with c3:
    contact = st.text_input("Contact Number")

c4,c5,c6 = st.columns(3)

with c4:
    village = st.text_input("Village")

with c5:
    bill = st.text_input("Bill Number")

with c6:
    selected_date = st.date_input("Date", value=date.today())

st.divider()

# ---------------- TABLE STRUCTURE ----------------

bags = 500
rows = ["W1","W2","W3","W4","W5","W6","W7","W8","W9","W10"]
columns = [str(i) for i in range(1, bags+1)]

# initialize table once
if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame(
        0,
        index=rows,
        columns=columns
    )

st.subheader("Potato Bag Weight Entry")

edited = st.data_editor(
    st.session_state.table_data,
    key="bag_table",
    use_container_width=True
)

# update session state
st.session_state.table_data = edited

# ---------------- CALCULATIONS ----------------

bag_totals = edited.sum(axis=0)
total_weight = edited.values.sum()
total_bags = (edited > 0).sum().sum()

display = edited.copy()
display.loc["Total"] = bag_totals

st.dataframe(display, use_container_width=True)

st.write("### Total Bags:", total_bags)
st.write("### Total Weight (kg):", total_weight)

st.divider()

# ---------------- SAVE FARMER RECORD ----------------

if st.button("Save Farmer Data to Excel"):

    record = {
        "Farmer Name": farmer,
        "Farmer ID": farmer_id,
        "Contact": contact,
        "Village": village,
        "Bill Number": bill,
        "Date": selected_date,
        "Total Bags": total_bags,
        "Total Weight": total_weight
    }

    df_record = pd.DataFrame([record])
    file_name = "farmer_records.xlsx"

    if os.path.exists(file_name):
        old = pd.read_excel(file_name)
        df_record = pd.concat([old, df_record], ignore_index=True)

    df_record.to_excel(file_name, index=False)

    st.success("Farmer data saved to Excel successfully")

# ---------------- RECEIPT ----------------

def generate_pdf():

    pdf = FPDF()
    pdf.add_page()

    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=60, y=10, w=80)

    pdf.ln(40)

    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"SOHAM TRADERS",0,1,"C")

    pdf.set_font("Arial","",12)

    pdf.cell(0,10,f"Farmer Name: {farmer}",0,1)
    pdf.cell(0,10,f"Farmer ID: {farmer_id}",0,1)
    pdf.cell(0,10,f"Contact: {contact}",0,1)
    pdf.cell(0,10,f"Village: {village}",0,1)
    pdf.cell(0,10,f"Bill Number: {bill}",0,1)
    pdf.cell(0,10,f"Date: {selected_date}",0,1)

    pdf.ln(5)

    pdf.cell(0,10,f"Total Bags: {total_bags}",0,1)
    pdf.cell(0,10,f"Total Weight: {total_weight} kg",0,1)

    pdf.output("receipt.pdf")

if st.button("Print Receipt"):

    generate_pdf()

    with open("receipt.pdf","rb") as f:

        st.download_button(
            "Download Receipt",
            data=f,
            file_name="receipt.pdf",
            mime="application/pdf"
        )
