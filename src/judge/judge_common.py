import pandas as pd

def evaluate_submit_df(submit_df, judge):

    res_list = []


    # submitサンプル各行に対してroopを回す
    for row_dict in submit_df.to_dict(orient="records"):
        print(row_dict)
        
        result = judge.judge(row_dict)

        for key, val in result.items():
            row_dict[key] = val

        res_list.append(row_dict)
    
    return pd.DataFrame(res_list)
    