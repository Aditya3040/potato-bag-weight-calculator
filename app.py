import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import os

st.set_page_config(page_title="Potato Bag Calculator", layout="wide")

# =========================
# HEADER WITH LOGO
# =========================

st.image("logo.png", width=250)

st.markdown("<h1 style='text-align:center;'>SOHAM TRADERS</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Mob - 9763916101 / 9021653848</h4>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>PepsiCo India Holdings Pvt Ltd</h3>", unsafe_allow_html=True)

st.divider()

# =========================
# FARMER INFORMATION
# =========================

st.subheader("Farmer Information")

col1, col2, col3 = st.columns(3)

with col1:
    farmer_name = st.text_input("Farmer Name")

with col2:
    farmer_id = st.text_input("Farmer ID")

with col3:
    contact = st.text_input("Contact Number")

col4, col5, col6 = st.columns(3)

with col4:
    village = st.text_input("Village Name")

with col5:
    bill_no = st.text_input("Bill Number")

with col6:
    date = st.date_input("Date")

st.divider()

# =========================
# BAG WEIGHT ENTRY
# =========================

st.subheader("Potato Bag Weight Entry")

bags = st.number_input("Number of Bags", min_value=1, max_value=100, value=5)

total_weight = 0
bag_totals = []

for bag in range(1, bags + 1):

    st.markdown(f"### Bag {bag}")

    cols = st.columns(10)
    weights = []

    for i in range(10):
        w = cols[i].number_input(
            f"W{i+1}",
            key=f"{bag}_{i}",
            min_value=0,
            step=1
        )
        weights.append(w)

    bag_total = sum(weights)
    bag_totals.append(bag_total)

    st.success(f"Bag {bag} Total = {bag_total} kg")

    total_weight += bag_total

st.divider()

# =========================
# FINAL RESULT
# =========================

st.subheader("Final Calculation")

st.write("Total Bags:", bags)
st.write("Total Weight (kg):", total_weight)

st.divider()

# =========================
# SAVE FARMER RECORD
# =========================

if st.button("Save Farmer Record"):

    data = {
        "Date": date,
        "Farmer Name": farmer_name,
        "Farmer ID": farmer_id,
        "Contact": contact,
        "Village": village,
        "Bill Number": bill_no,
        "Total Bags": bags,
        "Total Weight": total_weight
    }

    df = pd.DataFrame([data])

    if os.path.exists("farmers_record.csv"):
        old = pd.read_csv("farmers_record.csv")
        df = pd.concat([old, df], ignore_index=True)

    df.to_csv("farmers_record.csv", index=False)

    st.success("Farmer Record Saved Successfully")

# =========================
# PDF RECEIPT GENERATOR
# =========================

def generate_pdf():

    pdf = FPDF()
    pdf.add_page()

    # Logo
    pdf.image("logo.png", x=60, y=8, w=90)

    pdf.ln(50)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0,10,"SOHAM TRADERS",0,1,"C")

    pdf.set_font("Arial","",12)
    pdf.cell(0,10,"Mob - 9763916101 / 9021653848",0,1,"C")
    pdf.cell(0,10,"PepsiCo India Holdings Pvt Ltd",0,1,"C")

    pdf.ln(10)

    pdf.cell(0,10,f"Farmer Name: {farmer_name}",0,1)
    pdf.cell(0,10,f"Farmer ID: {farmer_id}",0,1)
    pdf.cell(0,10,f"Village: {village}",0,1)
    pdf.cell(0,10,f"Contact: {contact}",0,1)
    pdf.cell(0,10,f"Bill Number: {bill_no}",0,1)
    pdf.cell(0,10,f"Date: {date}",0,1)

    pdf.ln(10)

    pdf.cell(0,10,f"Total Bags: {bags}",0,1)
    pdf.cell(0,10,f"Total Weight: {total_weight} kg",0,1)

    pdf.output("receipt.pdf")

# =========================
# GENERATE RECEIPT BUTTON
# =========================

if st.button("Generate Printable Receipt"):

    generate_pdf()

    with open("receipt.pdf", "rb") as file:

        st.download_button(
            label="Download Receipt PDF",
            data=file,
            file_name="potato_receipt.pdf",
            mime="application/pdf"
        )
