import streamlit as st
import pandas as pd
import os
from fpdf import FPDF

st.set_page_config(page_title="Potato Bag Calculator", layout="wide")

# ----------------
# HEADER
# ----------------
if os.path.exists("logo.png"):
    st.image("logo.png", width=220)

st.markdown("<h2 style='text-align:center;'>SOHAM TRADERS</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Mob - 9763916101 / 9021653848</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>PepsiCo India Holdings Pvt Ltd</p>", unsafe_allow_html=True)

st.divider()

# ----------------
# FARMER INFO
# ----------------
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
    village = st.text_input("Village Name")

with c5:
    bill = st.text_input("Bill Number")

with c6:
    date = st.date_input("Date")

st.divider()

# ----------------
# TABLE STRUCTURE
# ----------------

bags = 1000
columns = ["R1","R2","R3","R4","R5","R6","R7","R8","R9","R10"]

if "table" not in st.session_state:

    st.session_state.table = pd.DataFrame(
        0,
        index=range(1,bags+1),
        columns=columns
    )

df = st.session_state.table.copy()
df.index.name = "Bag"

# calculate totals
df["Bag Total"] = df.sum(axis=1)

st.subheader("Potato Bag Weight Entry")

edited = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed",
    disabled=["Bag Total"]
)

# save edits
st.session_state.table = edited[columns]

# ----------------
# CALCULATIONS
# ----------------

bag_totals = edited[columns].sum(axis=1)

total_weight = bag_totals.sum()

total_bags = (bag_totals > 0).sum()

st.write("### Total Bags:", total_bags)
st.write("### Total Weight (kg):", total_weight)

st.divider()

# ----------------
# SAVE RECORD
# ----------------

if st.button("Save Farmer Record"):

    record = {
        "Farmer": farmer,
        "Village": village,
        "Contact": contact,
        "Bill": bill,
        "Total Bags": total_bags,
        "Total Weight": total_weight
    }

    rec = pd.DataFrame([record])

    if os.path.exists("farmers_record.csv"):
        old = pd.read_csv("farmers_record.csv")
        rec = pd.concat([old,rec])

    rec.to_csv("farmers_record.csv",index=False)

    st.success("Farmer Record Saved")

# ----------------
# PRINT RECEIPT
# ----------------

def generate_pdf():

    pdf = FPDF()
    pdf.add_page()

    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=60, y=8, w=90)

    pdf.ln(45)

    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"SOHAM TRADERS",0,1,"C")

    pdf.set_font("Arial","",12)
    pdf.cell(0,10,"Mob - 9763916101 / 9021653848",0,1,"C")
    pdf.cell(0,10,"PepsiCo India Holdings Pvt Ltd",0,1,"C")

    pdf.ln(10)

    pdf.cell(0,10,f"Farmer: {farmer}",0,1)
    pdf.cell(0,10,f"Village: {village}",0,1)
    pdf.cell(0,10,f"Contact: {contact}",0,1)
    pdf.cell(0,10,f"Bill: {bill}",0,1)
    pdf.cell(0,10,f"Date: {date}",0,1)

    pdf.ln(10)

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
