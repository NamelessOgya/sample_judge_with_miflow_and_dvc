# ① タイムスタンプ取得
timestamp=$(date +%Y%m%d%H%M%S)

# ② ハッシュ生成（SHA-1 or SHA-256 どちらでも可）
hash=$(echo -n "$timestamp" | sha1sum | cut -c1-12)
run_id="exp_${hash}"

echo "=========================="
echo "experinent id: $run_id"
echo "=========================="


poetry run dvc repro --params run.id="$run_id"

git add .
git commit -m "Auto: Run experiment with id: $run_id"
git tag $run_id