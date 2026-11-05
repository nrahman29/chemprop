from pathlib import Path

import joblib
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Project paths
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "delaney-processed.csv"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "esol_random_forest.joblib"

# Features used by the model
FEATURES = [
    "MolWt",
    "LogP",
    "HBD",
    "HBA",
    "TPSA",
    "RotatableBonds",
    "Rings",
]

TARGET = "measured log solubility in mols per litre"


def calculate_descriptors(smiles):
    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    return {
        "MolWt": Descriptors.MolWt(mol),
        "LogP": Descriptors.MolLogP(mol),
        "HBD": Descriptors.NumHDonors(mol),
        "HBA": Descriptors.NumHAcceptors(mol),
        "TPSA": Descriptors.TPSA(mol),
        "RotatableBonds": Descriptors.NumRotatableBonds(mol),
        "Rings": Descriptors.RingCount(mol),
    }


def main():
    print("Loading ESOL dataset...")
    df = pd.read_csv(DATA_PATH)

    print(f"Dataset rows: {len(df)}")

    # Calculate molecular descriptors
    descriptors = df["smiles"].apply(calculate_descriptors)
    valid = descriptors.notna()

    X = pd.DataFrame(descriptors[valid].tolist(), index=df.index[valid])
    y = df.loc[valid, TARGET]

    print(f"Valid molecules: {len(X)}")

    # Reproduce the original random 80/20 split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train Random Forest
    print("Training Random Forest...")
    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train[FEATURES], y_train)

    # Evaluate
    predictions = model.predict(X_test[FEATURES])

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    print("\nTest-set performance")
    print(f"MAE:  {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"R²:   {r2:.3f}")

    # Retrain final deployment model on the complete dataset
    model.fit(X[FEATURES], y)
    print("\nFinal model trained on all 1,128 molecules.")

    # Save model and feature names
    MODEL_DIR.mkdir(exist_ok=True)

    joblib.dump(
        {"model": model, "features": FEATURES},
        MODEL_PATH,
    )

    print(f"\nModel saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
