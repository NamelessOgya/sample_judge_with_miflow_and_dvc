"""
    poetry run python -m src.make_dashboard.generate_step_dashboard
"""


import mlflow
import pandas as pd
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))

def make_generate_dashboard_df(client):
    experiment_id = client.get_experiment_by_name("text_generation").experiment_id
    
    runs = client.search_runs(
        experiment_ids=[experiment_id],
        filter_string="",
        run_view_type=mlflow.entities.ViewType.ACTIVE_ONLY,
        max_results=1000,
    )

    # データをDataFrameに変換
    data = []
    for run in runs:
        try:
            result_dict = {
                "mikoto_run_id": run.data.params.get('mikoto_run_id'),
                "start_time": datetime.fromtimestamp(run.info.start_time / 1000, tz=JST) if run.info.start_time else None,
                "end_time": datetime.fromtimestamp(run.info.end_time / 1000, tz=JST) if run.info.end_time else None ,

                "generate_prompt_name": run.data.params.get('prompt_name'),
                "generate_prompt_base": run.data.params.get('generate_prompt_base'),
                "generate_prompt_version": run.data.params.get('generate_prompt_version'),
                "inference_model": run.data.params.get('model_config_model'),
            }

            data.append(result_dict)
        except:
            pass
    
    df = pd.DataFrame(data)

    
    return {
        "generate_history": df
    }

if __name__ == "__main__":
    # ログディレクトリのパス（UI起動時の backend-store-uri と同じ）
    tracking_uri = "./mlruns"
    mlflow.set_tracking_uri(tracking_uri)

    client = mlflow.tracking.MlflowClient()

    res_dict = make_evaluate_dashboard_df(client)

    for key, value in res_dict.items():
        print(f"====== {key} ======")

        print(value.head(5))

