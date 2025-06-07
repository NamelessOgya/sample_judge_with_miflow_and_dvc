"""
    poetry run python -m run.evaluate
"""

import pandas as pd

from src.sample_judge.llm_judge import LLMJudge


if __name__ == '__main__':
    submit = pd.read_csv("./data/submit/submit.csv") # todo: config指定できるように

    eval_pronpt_path_list = [
        "./src/sample_judge/prompt/check_if_category_in_text.txt",
        "./src/sample_judge/prompt/check_if_zokusei_in_text.txt"
    ]

    # 検証用のpronptすべてに対してroopを回す。
    for eval_pronpt_path in eval_pronpt_path_list:
        judge = LLMJudge(eval_pronpt_path)

        # submitサンプル各行に対してroopを回す
        for row_dict in submit.to_dict(orient="records"):
            
            prompt_path = "./src/sample_judge/prompt/check_if_category_in_text.txt"
            
            result = judge.judge(row_dict)
            print("==============================")
            print("=== row_dict ===")
            print(row_dict)

            print("== pronpt ==")
            print(judge.prompt_filling(row_dict))

            print("== result ==")
            print(result)

            row_dict["prompt"] = judge.prompt_filling(row_dict)
            row_dict["result"] = result["score"]
            row_dict["reason"] = result["reason"]