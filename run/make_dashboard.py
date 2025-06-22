
import mlflow
import pandas as pd
from src.make_dashboard.evaluate_step_dashbord import make_evaluate_dashboard_df
from src.make_dashboard.generate_step_dashboard import make_generate_dashboard_df

def main():
    # ログディレクトリのパス（UI起動時の backend-store-uri と同じ）
    tracking_uri = "./mlruns"
    mlflow.set_tracking_uri(tracking_uri)

    client = mlflow.tracking.MlflowClient()

    # generateのdashboard
    dic = make_evaluate_dashboard_df(client)
    
    for key, value in dic.items():
        value.to_csv(f"./data/dashboard/{key}.csv")


    # evaluateのdashboard
    dic = make_generate_dashboard_df(client)

    for key, value in dic.items():
        value.to_csv(f"./data/dashboard/{key}.csv")

    
    


if __name__ == "__main__":
    main()
