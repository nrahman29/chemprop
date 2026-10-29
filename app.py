
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw

st.set_page_config(page_title="ChemProp", page_icon="🧪")

st.title("🧪 ChemProp")
st.write("Predict aqueous solubility from molecular structures.")

@st.cache_resource
def load_model():
    path = Path(__file__).parent / "models" / "esol_random_forest.joblib"
    return joblib.load(path)

def calculate_descriptors(mol):
    return {
        "MolWt": Descriptors.MolWt(mol),
        "LogP": Descriptors.MolLogP(mol),
        "HBD": Descriptors.NumHDonors(mol),
        "HBA": Descriptors.NumHAcceptors(mol),
        "TPSA": Descriptors.TPSA(mol),
        "RotatableBonds": Descriptors.NumRotatableBonds(mol),
        "Rings": Descriptors.RingCount(mol)
    }

smiles = st.text_input("Enter SMILES", value="CCO")

if st.button("Predict"):
    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        st.error("Invalid SMILES string.")
    else:
        st.image(Draw.MolToImage(mol, size=(350, 250)))

        saved = load_model()
        features = pd.DataFrame(
            [calculate_descriptors(mol)]
        )[saved["features"]]

        prediction = saved["model"].predict(features)[0]

        st.metric("Predicted logS (mol/L)", f"{prediction:.3f}")
        st.dataframe(features.T.rename(columns={0: "Value"}))

        st.caption(
            "Predictions are estimates based on the ESOL dataset. "
            "Accuracy may be lower for unfamiliar molecular structures."
        )
