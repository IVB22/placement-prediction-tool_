import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "campus_recruitment.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "placement_model.pkl")

# ---------------- LOAD DATA ----------------
df = pd.read_csv(DATA_PATH)

# Target column
target_col = "status" if "status" in df.columns else "placed"

# Convert target to binary
y = df[target_col].astype(str).str.lower().map(
    lambda x: 1 if x in ["placed", "1", "yes", "y"] else 0
)

X = df.drop(columns=[target_col])

# Identify column types
cat_cols = [c for c in X.columns if X[c].dtype == "object"]
num_cols = [c for c in X.columns if c not in cat_cols]

# ---------------- PREPROCESSORS ----------------
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, num_cols),
        ("cat", categorical_transformer, cat_cols)
    ]
)

# ---------------- MODEL ----------------
model = LogisticRegression(max_iter=2000)

pipeline = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("classifier", model)
])

# ---------------- TRAIN ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipeline.fit(X_train, y_train)

# ---------------- SAVE ----------------
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(pipeline, MODEL_PATH)

print("✅ Model trained successfully with missing-value handling")
print("✅ Saved model to:", MODEL_PATH)
