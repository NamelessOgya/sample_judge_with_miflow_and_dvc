
"""
    rulebase judgeで使用する関数群をここに書いていく。 
    IFはかならず以下の値とする。 

    input: 
        string: str llmの出力

    config_dict: 
        config_dict: dict 検証用csv一行を辞書化したもの。
"""

def count_text_length(
    row_dict: dict
):
    return {"score": len(row_dict["text"])}