import pandas as pd
from src.utils.dvc_util import get_current_run_id

def generate_test_df(generate_target, invoker):

    res_list = []


    # submitサンプル各行に対してroopを回す
    for row_dict in generate_target.to_dict(orient="records"):
        print(row_dict)
        
        result = invoker.generate_row(row_dict)

        row_dict["mikoto_run_id"] = get_current_run_id()
        row_dict["text"] = result
        

        res_list.append(row_dict)
    
    return pd.DataFrame(res_list)