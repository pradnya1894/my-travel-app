import streamlit as st
import pandas as pd
import os
from datetime import date

# फाईलचे नाव जिथे सर्व डेटा सेव्ह होईल
FILE_NAME = "travel_data.csv"

# जर फाईल नसेल तर ती तयार करणे
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["तारीख", "ग्राहक", "गाडी", "रूट", "भाडे", "ऍडव्हान्स", "बाकी"])
    df.to_csv(FILE_NAME, index=False)

st.set_page_config(page_title="Travel Daily Report", layout="wide")

# --- SIDEBAR: डेटा एन्ट्री ---
st.sidebar.header("➕ नवीन नोंद")
with st.sidebar.form("my_form", clear_on_submit=True):
    d = st.date_input("तारीख", date.today())
    c = st.text_input("ग्राहकाचे नाव")
    v = st.selectbox("गाडी", ["Swift", "Ertiga", "Innova", "Traveller"])
    r = st.text_input("रूट")
    f = st.number_input("एकूण भाडे", min_value=0)
    a = st.number_input("ऍडव्हान्स", min_value=0)
    submit = st.form_submit_button("सेव्ह करा")

    if submit:
        new_data = pd.DataFrame([[d, c, v, r, f, a, f-a]], 
                                columns=["तारीख", "ग्राहक", "गाडी", "रूट", "भाडे", "ऍडव्हान्स", "बाकी"])
        new_data.to_csv(FILE_NAME, mode='a', header=False, index=False)
        st.sidebar.success("नोंद यशस्वी!")

# --- MAIN DASHBOARD ---
st.title("🚖 ट्रॅव्हल्स डेली रिपोर्ट")
df = pd.read_csv(FILE_NAME)

# आकडेवारी (Metrics)
col1, col2, col3 = st.columns(3)
col1.metric("एकूण बुकिंग", len(df))
col2.metric("एकूण उत्पन्न", f"₹{df['भाडे'].sum()}")
col3.metric("येणे बाकी रक्कम", f"₹{df['बाकी'].sum()}")

st.divider()

# डेटा टेबल
st.subheader("📑 सर्व रेकॉर्ड्स")
st.dataframe(df, use_container_width=True)

# डिलीट बटन (काही चुकले तर पूर्ण डेटा साफ करण्यासाठी)
if st.button("सर्व डेटा डिलीट करा"):
    os.remove(FILE_NAME)
    st.rerun()