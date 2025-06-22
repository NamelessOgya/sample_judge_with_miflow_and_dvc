"""
    poetry run python  -m src.make_dashboard.evaluate_step_dashbord
"""


import mlflow
import pandas as pd


def make_evaluate_dashboard_df(client):
    experiment_id = client.get_experiment_by_name("evaluate").experiment_id
    
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
                "submit": run.data.params.get('submit_file_name') + "_" + run.data.params.get('submit_file_version'),
                "mikoto_run_id": run.data.params.get('mikoto_run_id'),
                "score": run.data.metrics.get('score', None),
            }

            if run.data.params.get('category') == 'llm':
                result_dict["category"] = run.data.params.get('category')
                result_dict["judge_field"] = run.data.params.get('prompt_name') + "_" + run.data.params.get('judge_prompt_version')

                data.append(result_dict)
            elif run.data.params.get('category') == 'rulebase':
                result_dict["category"] = run.data.params.get('category')
                result_dict["judge_field"] = run.data.params.get('rulebase_func_name') + "_" + run.data.params.get('rulebase_func_version')

                data.append(result_dict)
            else:
                pass

            
        except:
            pass

    df = pd.DataFrame(data)

    # クロス集計例：learning_rate × batch_size ごとの accuracy 平均を出す
    print(df)
    scores = pd.pivot_table(df, index='submit', columns=['category', 'judge_field'], values='score', aggfunc='mean')

    # scores.to_csv("./data/dashboard/scores.csv")

    mikoto_run_ids = pd.pivot_table(
        df, 
        index='submit', 
        columns=['category', 'judge_field'], 
        values='mikoto_run_id', 
        aggfunc= lambda x: "; ".join(set(x))
    )

    # mikoto_run_ids.to_csv("./data/dashboard/mikoto_run_ids.csv")

    return {
        "scores": scores,
        "evaluate_mikoto_run_ids": mikoto_run_ids
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

