import json
from pathlib import Path
import pandas as pd
import streamlit as st

# Streamlit page configuration
st.set_page_config(
    page_title="Drug-Disease Link Predictor", page_icon="🧬", layout="wide"
)


st.markdown(
    """
    /* Background color for the entire app */
    <style>
    .stApp {
        background-color: #a18462; 
    }

    /* Caption text size */
    [data-testid="stCaptionContainer"] p {
        font-size: 1.1rem !important; 
    }
    """,
    unsafe_allow_html=True,
)

# Application Title & Information Note
st.title("🧬 Drug-Disease Link Predictor")
st.caption(
    "Predictions were generated based on Probabilistic Network Inference."
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



# 2. Search mode selection
search_mode = st.radio(
    "Select search mode:",
    options=["Search by Disease", "Search by Drug"],
    horizontal=True,
)

# 3. Dropdown menu with clear button ("X") and prediction results table display
if search_mode == "Search by Disease":
    if not diseases_data:
        st.error(
            "File 'diseases.json' was not found or is empty in the current directory."
        )
    else:
        disease_list = sorted(list(diseases_data.keys()))

        # Setting index=None adds an 'X' clear button inside the selectbox
        selected_disease = st.selectbox(
            "Select a Disease from the dropdown menu:",
            options=disease_list,
            index=None,
            placeholder="Type or select a disease to search...",
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

        # Setting index=None adds an 'X' clear button inside the selectbox
        selected_drug = st.selectbox(
            "Select a Drug from the dropdown menu:",
            options=drug_list,
            index=None,
            placeholder="Type or select a drug to search...",
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
    """
    <div style="
        background-color: #f5dfc6;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #EAE6DF;
        text-align: center;
        margin-top: 30px;
    ">
        <p style="color: #31333F; margin: 0; font-size: 1rem; font-weight: 500;">
            Developed by <b>Federica</b> | Master's Thesis Project
        </p>
        <p style="margin: 8px 0 0 0; font-size: 0.95rem;">
            🔗 <a href="https://github.com/federica13700" target="_blank" style="color: #0066cc; text-decoration: none;">GitHub Profile</a>
            &nbsp;•&nbsp;
            📁 <a href="https://github.com/federica13700/fab-app" target="_blank" style="color: #0066cc; text-decoration: none;">Project Repository</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
