import json
from pathlib import Path
import pandas as pd
import streamlit as st

# Configurazione standard della pagina
st.set_page_config(
    page_title="Drug-Disease Link Predictor",
    page_icon="🧬",
    layout="wide",
)

# Titolo e sottotitolo
st.title("🧬 Drug-Disease Link Predictor")
st.caption("Predictions were generated based on Probabilistic Network Inference.")


# 1. Caricamento dati JSON con cache per ottimizzare le prestazioni
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


# Carica i dati in memoria
drugs_data, diseases_data = load_data()

# 2. Selezione modalità di ricerca
search_mode = st.radio(
    "Select search mode:",
    options=["Search by Disease", "Search by Drug"],
    horizontal=True,
)

# 3. Logica di ricerca e visualizzazione risultati
if search_mode == "Search by Disease":
    if not diseases_data:
        st.error("File 'diseases.json' was not found or is empty in the current directory.")
    else:
        disease_list = sorted(list(diseases_data.keys()))
        selected_disease = st.selectbox(
            "Select a Disease from the dropdown menu:",
            options=disease_list,
            index=None,
            placeholder="Type or select a disease to search...",
        )

        if selected_disease:
            predictions = diseases_data.get(selected_disease, [])
            st.subheader(f"Predicted Candidate Drugs for: **{selected_disease}**")

            if predictions:
                df = pd.DataFrame(predictions)
                if "score" in df.columns:
                    df = df.drop(columns=["score"])

                df.index = [f"#{i+1}" for i in range(len(df))]
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No predictions found for the selected disease.")

else:
    if not drugs_data:
        st.error("File 'drugs.json' was not found or is empty in the current directory.")
    else:
        drug_list = sorted(list(drugs_data.keys()))
        selected_drug = st.selectbox(
            "Select a Drug from the dropdown menu:",
            options=drug_list,
            index=None,
            placeholder="Type or select a drug to search...",
        )

        if selected_drug:
            predictions = drugs_data.get(selected_drug, [])
            st.subheader(f"Predicted Candidate Diseases for: **{selected_drug}**")

            if predictions:
                df = pd.DataFrame(predictions)
                if "score" in df.columns:
                    df = df.drop(columns=["score"])

                df.index = [f"#{i+1}" for i in range(len(df))]
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No predictions found for the selected drug.")

# Sidebar laterale
st.sidebar.title("About fab-app")
st.sidebar.info(
    "**Drug-Disease Link Predictor** is an interactive tool for drug repurposing based on Probabilistic Network Inference. "
    "Predictions are inferred using 300 MCMC steps of a nested Degree-Corrected "
    "Stochastic Block Model (nDCSBM) on a bipartite network."
)

# Footer minimale standard
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 10px;">
        <p style="margin: 0;">Developed by <b>Federica</b> | Master's Thesis Project</p>
        <p style="margin: 5px 0 0 0;">
            🔗 <a href="https://github.com/federica13700" target="_blank">GitHub Profile</a>
            &nbsp;•&nbsp;
            📁 <a href="https://github.com/federica13700/fab-app" target="_blank">Project Repository</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)