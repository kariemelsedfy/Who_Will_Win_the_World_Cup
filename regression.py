import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error


def regression(trainYears, testYear):
    #Build training dataframe
    train_files = []
    for year in trainYears:
        train_files.append(f"TeamFeatures/{year}_features.csv")

    dfs = [pd.read_csv(f) for f in train_files]

    train_df = pd.concat(dfs, ignore_index=True)


    X_train = train_df.drop(["team", "success_score", "year"], axis=1)
    y_train = train_df["success_score"]


    #standardize
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)


    model = LinearRegression()

    model.fit(X_train_scaled, y_train)


    test_df = pd.read_csv(f"TeamFeatures/{testYear}_features.csv")

    X_test = test_df.drop(["team", "success_score", "year"], axis=1) 

    standardized_pred = scaler.transform(X_test)

    pred = model.predict(standardized_pred)

    pred_min = pred.min()
    pred_max = pred.max()
    pred_norm = (pred - pred_min) / (pred_max - pred_min)

    test_df["predicted_success_score"] = pred
    test_df["predicted_success_score_normalized"] = pred_norm

    test_df[["team", "predicted_success_score", "predicted_success_score_normalized"]].sort_values(
        by="predicted_success_score", 
        ascending=False
    ).reset_index(drop=True).to_csv(f"Results/{testYear}_teams_predicted_success_scores.csv")

    



def compute_r2(years):
    results = []
    for year in years:
        real_results = pd.read_csv(f"TeamFeatures/{year}_features.csv")[["team", "success_score"]].sort_values(
            by="team"
        )
        predicted_results = pd.read_csv(f"Results/{year}_teams_predicted_success_scores.csv").sort_values(
            by="team"
        )

        predicted_results_normalized = pd.read_csv(f"Results/{year}_teams_predicted_success_scores.csv").sort_values(
            by="team"
        )


        r2 = r2_score(real_results["success_score"], predicted_results["predicted_success_score"])
        r2_normalized = r2_score(real_results["success_score"], predicted_results["predicted_success_score_normalized"])
        results.append({
            "year":year,
            "R2":r2,
            "R2_normalized":r2_normalized
        })

    result = pd.DataFrame(results)
    result.to_csv("Results/R2.csv")

    

if __name__ == "__main__":
    compute_r2([2010, 2014, 2018, 2022])

