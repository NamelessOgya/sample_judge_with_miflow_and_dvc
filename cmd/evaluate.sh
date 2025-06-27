# ① タイムスタンプ取得
timestamp=$(date +%Y%m%d%H%M%S)

# ② ハッシュ生成し、一時ファイルとして吐き出す。
hash=$(echo -n "$timestamp" | sha1sum | cut -c1-12)
mikoto_run_id="exp_${hash}"
echo "mikoto_run_id: \"$mikoto_run_id\"" > current_run.yaml

echo "=========================="
echo "mikoto run id: $mikoto_run_id"
echo "=========================="


poetry run dvc repro rulebase_evaluate llm_evaluate llm_pairwise_evaluate --single-item

git add .

# git commitするが、変更がない場合はスキップする。
if ! git diff --cached --quiet; then
    git commit -m "Auto: Run experiment with id: $mikoto_run_id"
    git tag "$mikoto_run_id"
else
    echo "No changes to commit. Skipping git commit and tag."
fi
