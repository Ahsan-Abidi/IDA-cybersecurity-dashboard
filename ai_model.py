from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(data):
    df = pd.DataFrame(data, columns=["timestamp","ip","username","status","flag"])

    df["status"] = df["status"].apply(lambda x: 1 if x=="FAILED" else 0)

    model = IsolationForest(contamination=0.2)
    df["anomaly"] = model.fit_predict(df[["status"]])

    df["ai_flag"] = df["anomaly"].apply(lambda x: "ATTACK" if x==-1 else "NORMAL")

    return df[["timestamp","ip","username","status","flag","ai_flag"]].values.tolist()