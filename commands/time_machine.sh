# ユーザーに入力を促す
echo "=========================="
echo "状況再現を行いたい mikoto_run_id を入力して下さい。:"
echo "=========================="
read exp_id


# 入力が空かどうかをチェック
if [[ -z "$exp_id" ]]; then
    echo "入力がありませんでした。"
    exit 0
fi


# 例: 復元処理や実験実行など
git checkout "$exp_id"
poetry run dvc pull