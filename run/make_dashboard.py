"""
    poetry run python -m run.make_dashboard 
"""

import mlflow
import pandas as pd


def main():
    # ログディレクトリのパス（UI起動時の backend-store-uri と同じ）
    tracking_uri = "./mlruns"
    mlflow.set_tracking_uri(tracking_uri)

    client = mlflow.tracking.MlflowClient()

    experiment_id = "0"  # Experiment ID を指定（例：デフォルトは "0"）

    runs = client.search_runs(
        experiment_ids=[experiment_id],
        filter_string="",
        run_view_type=mlflow.entities.ViewType.ACTIVE_ONLY,
        max_results=1000,
    )

    # データをDataFrameに変換
    data = []
    for run in runs:
        print(run)
        print(run.data.params)
        
        res = {
            run.params.prompt_name
        }

    df = pd.DataFrame(data)

    # クロス集計例：learning_rate × batch_size ごとの accuracy 平均を出す
    pivot = pd.pivot_table(df, index='learning_rate', columns='batch_size', values='accuracy', aggfunc='mean')
    print(pivot)

if __name__ == "__main__":
    main()
