# AHC_template

## セットアップ

### 依存関係のインストール
```bash
pip install -r requirements.txt
```

### テストケースの生成
AHC001用のテストケースを自動的に生成できます（デフォルト100個）：

```bash
# 最も簡単：デフォルトで100個生成（シード0-99）
python download_testcases.py

# または個数を指定
python download_testcases.py --num-tests 50

# シード範囲を指定
python download_testcases.py --seeds 0-99

# 他のジェネレーターを使う場合
python download_testcases.py --generator tools/gen.exe --num-tests 100
```

このコマンドは以下を自動的に行います：
- 付属のPythonジェネレーター（`ahc001_generator.py`）を使用
- シード値から入力ファイルを生成（広告枠配置問題）
- ファイル名を`0000.txt`, `0001.txt`, ... の形式で保存
- `in/`ディレクトリに保存

**注意**: `ahc001_generator.py`はAHC001の仕様に基づいたPython実装です。
参考: https://kenkoooo.github.io/ahc001-gen-vis-wasm/

## 使い方
以下のコマンドを参考に、AHC提出用のスクリプトを引数で指定してdebug.pyを実行することで各テストケースを実行することができる。

``` bash
python debug.py --module_name scripts.sample --test_id 0 --epsilon 0.1 cooling_rate 0.1 epoch 100
```
- あるハイパーパラメータを設定して各テストケースでソルバーを実行する
- 出力ログを残したい場合は上記のコマンドを使用

``` bash
python optimizer.py
```
- configで指定したscriptsのハイパーパラメータ探索を行う
- 出力ログは残らない

### 留意点
- scriptには自作したsolve()を含む必要がある、main()はdebug.pyが使用する用なので基本変更する必要はない
- scriptごとに適したconfig.yamlをconf内に作成してもらう
    - cfg.optimizerを自作solverに与える


## 機能

### debug.py


### optimzer.py
- 複数のテストケースを自動で並列に実行
- optunaでのパラメータ最適化
- mlflowで実験記録、スコアの可視化を保存(予定)