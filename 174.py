import hashlib
import streamlit as st
from datetime import date

# Function to generate a hash for visit record
def generate_hash(patient_name, treatment, cost, date_of_visit):
    visit_data = patient_name + treatment + str(cost) + str(date_of_visit)
    visit_hash = hashlib.sha256(visit_data.encode()).hexdigest()
    return visit_hash

# Initialize the hospital ledger in session state if not already present
if "hospital_ledger_advanced" not in st.session_state:
    st.session_state.hospital_ledger_advanced = {}

# Title
st.title("🏥 Advanced Hospital Ledger")

# Sidebar form for adding a new patient visit
with st.sidebar.form("visit_form"):
    st.subheader("Add Patient Visit")
    patient_name = st.text_input("Patient Name")
    treatment = st.text_input("Treatment Received")
    cost = st.number_input("Treatment Cost ($)", min_value=0.0, step=0.01)
    date_of_visit = st.date_input("Date of Visit", value=date.today())

    submitted = st.form_submit_button("Add Visit")

    if submitted:
        if patient_name and treatment:
            # Generate hash
            visit_hash = generate_hash(patient_name, treatment, cost, date_of_visit)

            # Create the visit record
            visit = {
                "patient_name": patient_name,
                "treatment": treatment,
                "cost": cost,
                "date_of_visit": str(date_of_visit),
                "visit_hash": visit_hash
            }

            # Add visit to ledger
            ledger = st.session_state.hospital_ledger_advanced
            if patient_name not in ledger:
                ledger[patient_name] = []
            ledger[patient_name].append(visit)

            st.success(f"Visit added for {patient_name} on {date_of_visit} for treatment '{treatment}'.")
            st.info(f"Visit hash: {visit_hash}")
        else:
            st.error("Please fill in both patient name and treatment.")

# Display the ledger
st.header("📋 Advanced Hospital Ledger")

ledger = st.session_state.hospital_ledger_advanced
if ledger:
    for patient, visits in ledger.items():
        st.subheader(f"Patient: {patient}")
        for visit in visits:
            st.markdown(f"- **Treatment**: {visit['treatment']}, "
                        f"**Cost**: ${visit['cost']:.2f}, "
                        f"**Date**: {visit['date_of_visit']}, "
                        f"**Hash**: `{visit['visit_hash']}`")
else:
    st.write("No visits recorded yet.")
