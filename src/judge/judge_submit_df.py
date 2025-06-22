import pandas as pd
from src.judge.rulebase_judge import RulebaseJudge
from src.common.llm_invoker import LLMInvoker

def evaluate_submit_df(
        submit_df: pd.DataFrame, 
        judge: RulebaseJudge | LLMInvoker
    ):
    """
        evaluation用のsubmit_dfを受け取り、judgeを適用して結果を返す関数
        rulebase_judgeとllm_judgeのどちらも受け入れる。 

        rulebase_judgeの場合は、RulebaseJudge
        llm_judgeの場合は、LLMInvoker
        のインスタンスを受け取る。

        RulebaseJudge / LLMInvokerのjudgeメソッドは
        submitデータの行辞書形式を受け取りresult dictで返すことになっているので、
        処理を共通化できる。
    """

    res_list = []

    # submitサンプル各行に対してroopを回す
    for row_dict in submit_df.to_dict(orient="records"):
        print(row_dict)
        
        result = judge.judge(row_dict)

        for key, val in result.items():
            row_dict[key] = val

        res_list.append(row_dict)
    
    return pd.DataFrame(res_list)
    