import json
from pathlib import Path
import pandas as pd
import streamlit as st

# Streamlit page configuration
st.set_page_config(
    page_title="Drug-Disease Link Predictor", page_icon="🧬", layout="wide"
)


# 1. Load JSON data files with caching to optimize performance
@st.cache_data
def load_data():
    drugs_file = Path("drugs.json")
    diseases_file = Path("diseases.json")

    drugs_data = {}
    diseases_data = {}

    if drugs_file.exists():
        with open(drugs_file, "r", encoding="utf-8") as f:
            drugs_data = json.load(f)

    if diseases_file.exists():
        with open(diseases_file, "r", encoding="utf-8") as f:
            diseases_data = json.load(f)

    return drugs_data, diseases_data


# Load data into memory
drugs_data, diseases_data = load_data()

# Application Title & Information Note
st.title("🧬 Drug-Disease Link Predictor")
st.caption(
    "Predictions were generated based on Probabilistic Network Inference."
)

# 2. Search mode selection
search_mode = st.radio(
    "Select search mode:",
    options=["Search by Disease", "Search by Drug"],
    horizontal=True,
)

# 3. Dropdown menu and prediction results table display
if search_mode == "Search by Disease":
    if not diseases_data:
        st.error(
            "File 'diseases.json' was not found or is empty in the current directory."
        )
    else:
        disease_list = sorted(list(diseases_data.keys()))
        selected_disease = st.selectbox(
            "Select a Disease from the dropdown menu:",
            options=disease_list,
            index=0,
        )

        if selected_disease:
            predictions = diseases_data.get(selected_disease, [])
            st.subheader(
                f"Predicted Candidate Drugs for: **{selected_disease}**"
            )

            if predictions:
                df = pd.DataFrame(predictions)
                # Hide prediction scores from the output table
                if "score" in df.columns:
                    df = df.drop(columns=["score"])

                df.index = [f"#{i+1}" for i in range(len(df))]
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No predictions found for the selected disease.")

else:
    if not drugs_data:
        st.error(
            "File 'drugs.json' was not found or is empty in the current directory."
        )
    else:
        drug_list = sorted(list(drugs_data.keys()))
        selected_drug = st.selectbox(
            "Select a Drug from the dropdown menu:",
            options=drug_list,
            index=0,
        )

        if selected_drug:
            predictions = drugs_data.get(selected_drug, [])
            st.subheader(
                f"Predicted Candidate Diseases for: **{selected_drug}**"
            )

            if predictions:
                df = pd.DataFrame(predictions)
                # Hide prediction scores from the output table
                if "score" in df.columns:
                    df = df.drop(columns=["score"])

                df.index = [f"#{i+1}" for i in range(len(df))]
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No predictions found for the selected drug.")


st.sidebar.title("About fab-app")
st.sidebar.info(
    "**Drug-Disease Link Predictor** is an interactive tool for drug repurposing based on Probabilistic Network Inference. "
    "Predictions are inferred using 300 MCMC steps of a nested Degree-Corrected "
    "Stochastic Block Model (nDCSBM) on a bipartite network."
)

# --- MAIN PAGE FOOTER ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9em;'>"
    "Master's Thesis Project<br>"
    "🔗 <a href='https://github.com/federica13700' target='_blank'>GitHub Profile</a> • "
    "📁 <a href='https://github.com/federica13700/fab-app' target='_blank'>Project Repository</a>"
    "</div>",
    unsafe_allow_html=True,
)
