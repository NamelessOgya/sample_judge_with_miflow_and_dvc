import pandas as pd

def generate_test_df(generate_target, invoker):

    res_list = []


    # submitサンプル各行に対してroopを回す
    for row_dict in generate_target.to_dict(orient="records"):
        print(row_dict)
        
        result = invoker.generate_row(row_dict)

        row_dict["text"] = result

        res_list.append(row_dict)
    
    return pd.DataFrame(res_list)