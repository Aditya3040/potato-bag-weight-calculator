import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Potato Bag Weight Calculator", layout="wide")

# ======================
# HEADER
# ======================

if os.path.exists("logo.png"):
    st.image("logo.png", width=220)

st.markdown("<h2 style='text-align:center;'>SOHAM TRADERS</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Mob - 9763916101 / 9021653848</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>PepsiCo India Holdings Pvt Ltd</p>", unsafe_allow_html=True)

st.divider()

# ======================
# FARMER DETAILS
# ======================

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

# ======================
# BAG TABLE
# ======================

rows = 1000

cols = ["W1","W2","W3","W4","W5","W6","W7","W8","W9","W10"]

df = pd.DataFrame(0, index=range(1, rows+1), columns=cols)

df.index.name = "Bag"

st.subheader("Potato Bag Weight Entry")

edited = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed",
)

# ======================
# CALCULATIONS
# ======================

weight_cols = cols

bag_totals = edited.sum(axis=1)

result = edited.copy()
result["Bag Total"] = bag_totals

# count bags where weight entered
total_bags = (bag_totals > 0).sum()

# overall weight
total_weight = bag_totals.sum()

st.subheader("Bag Table With Totals")

st.dataframe(result, use_container_width=True)

st.divider()

# ======================
# FINAL RESULT
# ======================

st.markdown(f"### Total Bags: **{total_bags}**")

st.markdown(f"### Total Weight (kg): **{total_weight}**")

st.divider()

# ======================
# SAVE RECORD
# ======================

if st.button("Save Farmer Record"):

    record = {
        "Farmer": farmer,
        "Village": village,
        "Contact": contact,
        "Bill": bill,
        "Total Bags": total_bags,
        "Total Weight": total_weight
    }

    rec_df = pd.DataFrame([record])

    if os.path.exists("farmers_record.csv"):
        old = pd.read_csv("farmers_record.csv")
        rec_df = pd.concat([old,rec_df])

    rec_df.to_csv("farmers_record.csv", index=False)

    st.success("Farmer Record Saved Successfully")
