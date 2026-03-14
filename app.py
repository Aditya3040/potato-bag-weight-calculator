import streamlit as st
import pandas as pd
import os
from fpdf import FPDF

st.set_page_config(page_title="Potato Bag Calculator", layout="wide")

# ======================
# HEADER
# ======================

if os.path.exists("logo.png"):
    st.image("logo.png", width=250)

st.markdown("<h1 style='text-align:center;'>SOHAM TRADERS</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Mob - 9763916101 / 9021653848</h4>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>PepsiCo India Holdings Pvt Ltd</h3>", unsafe_allow_html=True)

st.divider()

# ======================
# FARMER INFO
# ======================

st.subheader("Farmer Information")

c1,c2,c3 = st.columns(3)

with c1:
    farmer_name = st.text_input("Farmer Name")

with c2:
    farmer_id = st.text_input("Farmer ID")

with c3:
    contact = st.text_input("Contact Number")

c4,c5,c6 = st.columns(3)

with c4:
    village = st.text_input("Village Name")

with c5:
    bill_no = st.text_input("Bill Number")

with c6:
    date = st.date_input("Date")

st.divider()

# ======================
# POTATO BAG TABLE
# ======================

st.subheader("Potato Bag Weight Entry")

bags = 1000

columns = ["Bag","W1","W2","W3","W4","W5","W6","W7","W8","W9","W10","Bag Total"]

data = []

for i in range(1,bags+1):
    row = [i,0,0,0,0,0,0,0,0,0,0,0]
    data.append(row)

df = pd.DataFrame(data,columns=columns)

edited_df = st.data_editor(
    df,
    use_container_width=True,
    disabled=["Bag","Bag Total"]
)

# ======================
# CALCULATE BAG TOTAL
# ======================

weight_cols = ["W1","W2","W3","W4","W5","W6","W7","W8","W9","W10"]

edited_df["Bag Total"] = edited_df[weight_cols].sum(axis=1)

total_weight = edited_df["Bag Total"].sum()

st.write("### Total Bags:",bags)
st.write("### Total Weight (kg):",total_weight)

st.divider()

# ======================
# SAVE FARMER RECORD
# ======================

if st.button("Save Farmer Record"):

    record = {
        "Farmer": farmer_name,
        "Village": village,
        "Contact": contact,
        "Bill": bill_no,
        "Bags": bags,
        "Total Weight": total_weight
    }

    df_record = pd.DataFrame([record])

    if os.path.exists("farmers_record.csv"):
        old = pd.read_csv("farmers_record.csv")
        df_record = pd.concat([old,df_record])

    df_record.to_csv("farmers_record.csv",index=False)

    st.success("Record Saved Successfully")

# ======================
# PDF RECEIPT
# ======================

def generate_pdf():

    pdf = FPDF()
    pdf.add_page()

    if os.path.exists("logo.png"):
        pdf.image("logo.png",x=60,y=8,w=90)

    pdf.ln(50)

    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"SOHAM TRADERS",0,1,"C")

    pdf.set_font("Arial","",12)
    pdf.cell(0,10,"Mob - 9763916101 / 9021653848",0,1,"C")
    pdf.cell(0,10,"PepsiCo India Holdings Pvt Ltd",0,1,"C")

    pdf.ln(10)

    pdf.cell(0,10,f"Farmer: {farmer_name}",0,1)
    pdf.cell(0,10,f"Village: {village}",0,1)
    pdf.cell(0,10,f"Contact: {contact}",0,1)
    pdf.cell(0,10,f"Bill: {bill_no}",0,1)

    pdf.ln(10)

    pdf.cell(0,10,f"Total Bags: {bags}",0,1)
    pdf.cell(0,10,f"Total Weight: {total_weight} kg",0,1)

    pdf.output("receipt.pdf")

if st.button("Generate Receipt"):

    generate_pdf()

    with open("receipt.pdf","rb") as f:

        st.download_button(
            "Download Receipt",
            data=f,
            file_name="receipt.pdf",
            mime="application/pdf"
        )
