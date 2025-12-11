import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error


train_files = [
    "TeamFeatures/2010_features.csv",
    "TeamFeatures/2014_features.csv",
    "TeamFeatures/2018_features.csv",
    "TeamFeatures/2022_features.csv",
]

dfs = [pd.read_csv(f) for f in train_files]

train_df = pd.concat(dfs, ignore_index=True)


X_train = train_df.drop(["team", "success_score", "year"], axis=1)
y_train = train_df["success_score"]



scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)


model = LinearRegression()

model.fit(X_train_scaled, y_train)


test_df = pd.read_csv("TeamFeatures/2026_features.csv")

X_2026 = test_df.drop(["team", "success_score", "year"], axis=1) 

standardized_pred = scaler.transform(X_2026)


pred_2026 = model.predict(standardized_pred)


test_df["predicted_success_score"] = pred_2026

print(test_df[["team", "predicted_success_score"]])


importance = (
    pd.DataFrame({
        "feature": X_train.columns,
        "coef": model.coef_
    })
    .sort_values(by="coef", ascending=False)
)

print(importance)

