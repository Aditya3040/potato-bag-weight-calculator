import streamlit as st
import pandas as pd
import os
from fpdf import FPDF

st.set_page_config(page_title="Potato Bag Weight Calculator", layout="wide")

# ---------------------------
# HEADER
# ---------------------------
if os.path.exists("logo.png"):
    st.image("logo.png", width=220)

st.markdown("<h2 style='text-align:center;'>SOHAM TRADERS</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Mob - 9763916101 / 9021653848</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>PepsiCo India Holdings Pvt Ltd</p>", unsafe_allow_html=True)

st.divider()

# ---------------------------
# FARMER SEARCH / ENTRY
# ---------------------------
st.subheader("Farmer Information")

if os.path.exists("farmers_record.csv"):
    db = pd.read_csv("farmers_record.csv")
else:
    db = pd.DataFrame(columns=["Farmer","Village","Contact","Bill"])

search = st.text_input("Search Farmer")

if search:
    results = db[db["Farmer"].str.contains(search, case=False, na=False)]
    st.dataframe(results)

c1,c2,c3 = st.columns(3)

with c1:
    farmer = st.text_input("Farmer Name")

with c2:
    village = st.text_input("Village")

with c3:
    contact = st.text_input("Contact")

bill = st.text_input("Bill Number")

st.divider()

# ---------------------------
# CREATE BAG TABLE
# ---------------------------
bags = 1000
cols = ["W1","W2","W3","W4","W5","W6","W7","W8","W9","W10"]

df = pd.DataFrame(0, index=range(1, bags+1), columns=cols)
df.index.name = "Bag"

st.subheader("Potato Bag Weight Entry")

edited = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed",
    column_config={
        c: st.column_config.NumberColumn(c, step=1) for c in cols
    }
)

# ---------------------------
# LIVE TOTAL CALCULATION
# ---------------------------
bag_totals = edited.sum(axis=1)
total_weight = bag_totals.sum()

result = edited.copy()
result["Bag Total"] = bag_totals

st.subheader("Live Bag Totals")

st.dataframe(result, use_container_width=True)

st.write("### Total Bags:", bags)
st.write("### Total Weight (kg):", total_weight)

st.divider()

# ---------------------------
# SAVE FARMER RECORD
# ---------------------------
if st.button("Save Farmer Record"):

    record = {
        "Farmer": farmer,
        "Village": village,
        "Contact": contact,
        "Bill": bill,
        "Total Weight": total_weight
    }

    df_record = pd.DataFrame([record])

    if os.path.exists("farmers_record.csv"):
        old = pd.read_csv("farmers_record.csv")
        df_record = pd.concat([old,df_record])

    df_record.to_csv("farmers_record.csv",index=False)

    st.success("Record Saved")

# ---------------------------
# EXCEL EXPORT
# ---------------------------
excel = result.copy()
excel["Bag"] = excel.index

st.download_button(
    "Download Excel",
    data=excel.to_csv(index=False),
    file_name="potato_bag_weights.csv",
    mime="text/csv"
)

# ---------------------------
# PROFESSIONAL RECEIPT
# ---------------------------
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
