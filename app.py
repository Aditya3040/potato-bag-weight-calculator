import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
from datetime import date

st.set_page_config(page_title="Potato Bag Weight Calculator", layout="wide")

# ---------- HEADER ----------

if os.path.exists("logo.png"):
    st.image("logo.png", width=200)

st.markdown("## SOHAM TRADERS")
st.markdown("Mob - 9763916101 / 9021653848")
st.markdown("PepsiCo India Holdings Pvt Ltd")

st.divider()

# ---------- FARMER INFO ----------

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

# ---------- BAG ENTRY ----------

st.subheader("Potato Bag Weight Entry")

bags = st.number_input("Number of Bags", 1, 2000, 20)

if "weights" not in st.session_state:
    st.session_state.weights = {}

total_weight = 0
total_bags = 0

for bag in range(1, bags + 1):

    cols = st.columns(10)
    bag_total = 0

    for i in range(1, 11):

        key = f"{bag}_{i}"

        val = cols[i-1].text_input(
            f"W{i}",
            key=key,
            placeholder="0",
        )

        try:
            weight = float(val)
            bag_total += weight
            total_weight += weight
            if weight > 0:
                total_bags += 1
        except:
            weight = 0

    st.write(f"**Bag {bag} Total:** {bag_total}")

st.divider()

st.write("### Total Bags:", total_bags)
st.write("### Total Weight (kg):", total_weight)

st.divider()

# ---------- SAVE FARMER DATA ----------

file_name = "farmer_records.xlsx"

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

    if os.path.exists(file_name):
        old = pd.read_excel(file_name)
        df_record = pd.concat([old, df_record], ignore_index=True)

    df_record.to_excel(file_name, index=False)

    st.success("Farmer data saved successfully")

# ---------- DOWNLOAD EXCEL ----------

if os.path.exists(file_name):

    with open(file_name, "rb") as f:

        st.download_button(
            "Download Farmer Records Excel",
            data=f,
            file_name="farmer_records.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ---------- VIEW SAVED FARMER DATA ----------

if os.path.exists(file_name):

    st.subheader("Saved Farmer Records")

    data = pd.read_excel(file_name)

    st.dataframe(data, use_container_width=True)

# ---------- PROFESSIONAL RECEIPT ----------

def generate_pdf():

    pdf = FPDF()
    pdf.add_page()

    # Load custom fonts
    pdf.add_font("DejaVu","", "DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu","B", "DejaVuSans-Bold.ttf", uni=True)

    # ---------- LOGO ----------
    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=75, y=10, w=60)

    pdf.ln(50)

    # ---------- COMPANY NAME ----------
    pdf.set_font("DejaVu","B",20)
    pdf.cell(0,10,"SOHAM TRADERS",0,1,"C")

    pdf.set_font("DejaVu","",12)
    pdf.cell(0,8,"Mob: 9763916101 / 9021653848",0,1,"C")
    pdf.cell(0,8,"PepsiCo India Holdings Pvt Ltd",0,1,"C")

    pdf.ln(10)

    pdf.line(10,pdf.get_y(),200,pdf.get_y())
    pdf.ln(10)

    # ---------- FARMER DETAILS ----------
    pdf.set_font("DejaVu","B",14)
    pdf.cell(0,10,"Farmer Details",0,1)

    pdf.set_font("DejaVu","",12)

    pdf.cell(50,8,"Farmer Name:",0)
    pdf.cell(0,8,str(farmer),0,1)

    pdf.cell(50,8,"Farmer ID:",0)
    pdf.cell(0,8,str(farmer_id),0,1)

    pdf.cell(50,8,"Contact:",0)
    pdf.cell(0,8,str(contact),0,1)

    pdf.cell(50,8,"Village:",0)
    pdf.cell(0,8,str(village),0,1)

    pdf.cell(50,8,"Bill Number:",0)
    pdf.cell(0,8,str(bill),0,1)

    pdf.cell(50,8,"Date:",0)
    pdf.cell(0,8,str(selected_date),0,1)

    pdf.ln(10)

    pdf.line(10,pdf.get_y(),200,pdf.get_y())
    pdf.ln(10)

    # ---------- TOTAL SECTION ----------
    pdf.set_font("DejaVu","B",14)
    pdf.cell(0,10,"Weight Summary",0,1)

    pdf.set_font("DejaVu","",12)

    pdf.cell(60,10,"Total Bags:",1,0)
    pdf.cell(0,10,str(total_bags),1,1)

    pdf.cell(60,10,"Total Weight (kg):",1,0)
    pdf.cell(0,10,str(total_weight),1,1)

    pdf.ln(20)

    pdf.set_font("DejaVu","",10)
    pdf.cell(0,8,"Thank you for doing business with Soham Traders",0,1,"C")

    pdf.output("receipt.pdf")

# ---------- PRINT RECEIPT ----------

if st.button("Print Receipt"):

    generate_pdf()

    with open("receipt.pdf","rb") as f:

        st.download_button(
            "Download Receipt",
            data=f,
            file_name="receipt.pdf",
            mime="application/pdf"
        )
