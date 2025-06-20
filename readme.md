
# 基本思想  
`git commit`の時のcommit idで学習データ・コードのバージョンを管理する。  
mlflowによりcommit idと実行結果の紐づけを行う。  
  
## 依存ファイルの設定  
```
poetry run dvc stage add -n evaluate \
  -d data/ \
  -d src/sample_judge/prompt \
  -d src/sample_judge/rule_base_judge \
  -o result/result.csv \
  python -m run.evaluate

```

## run  
```
poetry run dvc repro evaluate
```