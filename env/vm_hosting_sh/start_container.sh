#!/bin/bash
set -e

# もし同名コンテナが残っていれば消す
docker rm -f sample_judge_with_mlflow_and_dvc 2>/dev/null || true

# バックグラウンドで立ち上げ。tail で常駐させる
docker run -d \
  --gpus all \
  --name sample_judge_with_mlflow_and_dvc \
  -v "$(pwd):/app" \
  -w "/app" \
  --env CUDA_VISIBLE_DEVICES="" \
  --runtime=runc \
  --restart unless-stopped \
  my-pytorch-poetry:latest \
  tail -f /dev/null

exec docker exec -it sample_judge_with_mlflow_and_dvc bash