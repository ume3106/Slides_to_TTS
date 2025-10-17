# Google Slides スピーカーノート → TTS音声生成ツール

Google Slides のスピーカーノートから自動的に TTS（Text-to-Speech）音声ファイル（MP3）を生成する Python ツールです。

---

## 機能

* Google Slides のスピーカーノートを**自動抽出**
* **日本語音声合成**（Google Cloud Text-to-Speech API 使用）
* **句読点（。）後の自動ポーズ**挿入
* **スライドごとの個別 MP3** ファイル生成

---

## セットアップと環境構築

本ツールの実行には、Google Cloud Platform の設定（API の有効化、サービスアカウント、OAuth 認証）と Python 環境の構築が必要です。詳細は、同梱の **`SETUP_GUIDE.md`** を参照してください。

---

## インストール

### 1. Python 環境の準備

```bash
# Python 3.8以上が必要
python --version
```

### 2. 依存関係のインストール

作業フォルダに移動し、依存関係をインストールします。

```bash
pip install -r requirements.txt
```

---

## 使用方法

### 1. スピーカーノートの準備

Google Slides で各スライドのスピーカーノートに話す内容を記入してください。

### 2. プログラム実行

作業フォルダに移動し、可能であれば仮想環境をアクティベートした状態で実行してください。

```bash
# 1. 作業フォルダに移動 (Windowsの場合の例)
cd C:\Users\社員番号\Slides_to_Vids

# 2. 仮想環境をアクティベート (Windows/Mac/Linux)
# Windows:
# .\slides-tts-env\Scripts\activate
# macOS/Linux:
# source slides-tts-env/bin/activate

# 3. プログラムを実行
python generate_tts_from_slides.py
```

実行時に Google Slides の **URL** または **プレゼンテーションID** の入力を求められます。

### 3. 出力

* 初回実行時にブラウザで**認証**が必要です（`token.pickle` が生成されます）。
* 処理完了後、`slides/` フォルダに `slide_01.mp3`, `slide_02.mp3` などの音声ファイルが生成されます。

---

## 設定

`generate_tts_from_slides.py` を直接編集することで、音声設定をカスタマイズできます。

### 音声設定例

* **言語**: 日本語（`ja-JP`）
* **音声**: `ja-JP-Standard-B`（男性）
* **速度**: 1.1倍速
* **ポーズ**: 句読点（。）後に 1 秒のポーズ

```python
# 音声設定（generate_tts_from_slides.py 内の該当箇所）
voice = texttospeech.VoiceSelectionParams(language_code="ja-JP", name="ja-JP-Standard-B")
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=1.1)

# ポーズ設定
ssml_body = re.sub(r"。", "。<break time=\"1s\"/>", normalized)
```

---

## トラブルシューティング

詳細は `SETUP_GUIDE.md` の最後のセクションを参照してください。

### よくあるエラー

* **認証エラー**: `tts-key.json` や `token.pickle` の問題
* **API 有効化エラー**: `403 Forbidden` の問題
* **ファイルが見つからない**: `credentials.json` の配置問題

---

## ライセンス

このツールは**社内利用目的**で作成されています。

---

## サポート

問題が発生した場合は、`SETUP_GUIDE.md` のサポート情報をご確認ください。
