\# ChemProp: Molecular Solubility Prediction



A cheminformatics and machine-learning project investigating the prediction of aqueous solubility from molecular structure.



\## Project Objective



Predict experimentally measured aqueous solubility (logS in mol/L) using molecular descriptors calculated from SMILES representations with RDKit.



\## Dataset



Delaney ESOL dataset containing 1,128 molecules with experimentally measured aqueous solubilities.



\## Methodology



1\. Parse molecular SMILES using RDKit.

2\. Calculate seven molecular descriptors, including molecular weight, LogP, TPSA and hydrogen-bonding properties.

3\. Split the dataset into 80% training and 20% testing.

4\. Train Linear Regression and Random Forest models.

5\. Evaluate predictions using MAE, RMSE and R².

6\. Investigate molecular descriptor importance.



\## Results



| Model | MAE | RMSE | R² |

|---|---:|---:|---:|

| Linear Regression | 0.815 | 1.073 | 0.756 |

| Random Forest | 0.561 | 0.810 | 0.861 |



The Random Forest reduced the mean absolute prediction error by approximately 31% compared with Linear Regression on the random test split.



\## Technologies



Python, RDKit, pandas, NumPy, scikit-learn, Matplotlib and Jupyter Notebook.



\## Future Development



\- Permutation feature importance

\- Morgan molecular fingerprints

\- Scaffold-based train/test splitting

\- Hyperparameter optimization

\- Interactive molecular solubility prediction application



\## Limitations



The current results are based on a random train/test split. Further evaluation using molecular scaffold splitting and cross-validation is necessary to assess generalization to structurally different molecules.

