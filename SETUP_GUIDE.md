# セットアップガイド

このガイドでは、Google Slides TTS 生成ツールの初期設定手順を詳しく説明します。

---

## 前提条件

* Python **3.8以上**がインストールされていること

---

## 事前準備

任意の場所に**作業フォルダ**を作成してください。

**例**: `C:\Users\社員番号\Slides_to_Vids` フォルダを作成し、このフォルダ内にGitHubからダウンロードしたファイルを全て配置します。

---

## ステップ1: Google Cloud Console 設定

### 1.1 プロジェクトの作成

1. **Google Cloud Console(https://console.cloud.google.com/)** にアクセス
2. 上部の **プロジェクト選択**ドロップダウンをクリック
3. **「新しいプロジェクト」** をクリック
4. プロジェクト名を入力（例：`slides-tts-project`）
5. **「作成」** をクリック
6. 作成されたプロジェクトを**選択**

### 1.2 必要な API の有効化

1. 左メニュー **「APIとサービス」 → 「ライブラリ」** を選択
2. 以下の API を検索して**有効化**

   * **Google Slides API**

     * 検索ボックスに「Google Slides API」と入力
     * 「Google Slides API」をクリック → **「有効にする」**
   * **Cloud Text-to-Speech API**

     * 検索ボックスに「Cloud Text-to-Speech API」と入力
     * 「Cloud Text-to-Speech API」をクリック → **「有効にする」**

---

## ステップ2: サービスアカウント作成（TTS用）

### 2.1 サービスアカウントの作成

1. 左メニュー **「IAMと管理」 → 「サービスアカウント」** を選択
2. **「サービスアカウントを作成」** をクリック
3. 以下の情報を入力

   * **サービスアカウント名**: `slides-tts-service`
   * **サービスアカウントID**: 自動生成（変更可）
   * **説明**: `Google Slides TTS生成用サービスアカウント`
4. **「作成して続行」** をクリック
5. **ロールを選択** → 「**基本**」 → **「編集者（roles/editor）」** を選択
6. **「続行」** をクリック
7. **③ アクセス権を持つプリンシパル** は空のまま **「完了」**

### 2.2 キーファイルのダウンロード

1. 作成したサービスアカウントをクリック
2. **「鍵」タブ** → **「キーを追加」 → 「新しい鍵を作成」**
3. キータイプは **「JSON」** を選択 → **「作成」**
4. ダウンロードされた JSON ファイルを **`tts-key.json`** として作業フォルダに保存

> 🔐 **注意**: `tts-key.json` は機密情報です。社外・公開リポジトリにアップロードしないでください。

---

## ステップ3: OAuth 認証設定（Slides API 用）

### 3.1 OAuth 同意画面の設定

1. 左メニュー **「APIとサービス」 → 「OAuth同意画面」** を選択
2. 「Google Auth Platformはまだ構成されていません」と表示されたら **「開始」**
3. **アプリ情報**

   * アプリ名: `Slides TTS Generator`（任意）
   * ユーザーサポートメール: 自分のメールアドレス
4. **対象の選択**

   * **内部**（組織内利用） / **外部**（個人利用）いずれかを選択
5. **連絡先情報**: 自分のメールアドレスを入力
6. **ポリシー同意**: 「Google API サービス：ユーザーデータに関するポリシーに同意します」にチェック
7. **「続行」 → 「作成」** で同意画面の設定を完了

### 3.2 OAuth クライアント ID の作成

1. 左メニュー **「APIとサービス」 → 「認証情報」** を選択
2. **「認証情報を作成」 → 「OAuth クライアント ID」**
3. アプリケーションの種類: **「デスクトップアプリケーション」** を選択
4. 名前（例: `slides-reader`）を入力 → **「作成」**
5. **「JSONをダウンロード」** をクリックして保存
6. ダウンロードした JSON を **`credentials.json`** として作業フォルダに保存

> 🔐 **注意**: `credentials.json` も機密情報です。取り扱いに注意してください。

---

## ステップ4: Python 環境のセットアップ

> **注意**: 以下は **コマンドプロンプト（Windows）** または **ターミナル（macOS/Linux）** で実行します。

このツールは以下の Python ライブラリを使用します。

* `google-cloud-texttospeech`: Google Cloud Text-to-Speech API（音声合成）
* `google-api-python-client`: Google Slides API（スライド読み取り）
* `google-auth`: Google 認証ライブラリ
* `requests`: HTTP 通信ライブラリ

### 4.1 Python の確認

まず、Python 3.8 以上がインストールされているか確認します。
コマンドプロンプトで以下のコマンドを実行します。

```bash
python --version
```

Python 3.8 未満の場合は、Python 公式サイトから最新版をインストールしてください。

### 4.2 仮想環境の作成（推奨）

システムの Python 環境を汚さないため、専用の仮想環境を作成することを推奨します。

以下のコマンドを実行します。
> ℹ️ 社員番号はご自身のものに置き換えてください。

```bash
cd C:\Users\社員番号\Slides_to_Vids
```

次に仮想環境を作成します。
以下のコマンドを実行してください。

```bash
python -m venv slides-tts-env
```

最後に仮想環境をアクティベートします。
以下のコマンドを実行してください。

```bash
slides-tts-env\Scripts\activate
```

※macOS/Linuxの場合は以下のコマンドを実行してください。

```bash
source slides-tts-env/bin/activate
```

> ℹ️ 仮想環境をアクティベートすると、プロンプトの先頭に `(slides-tts-env)` が表示されます。

### 4.3 依存関係のインストール

仮想環境をアクティベートした状態で、必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

インストール後、主なライブラリの例（バージョンは一例）

```
google-cloud-texttospeech==2.16.3
google-api-python-client==2.108.0
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
requests==2.31.0
```

---

## ステップ5: ファイル構成の確認

最終的なファイル構成は以下のようになります。この状態になっているか確認してください。

```text
Slides_to_Vids/
├── generate_tts_from_slides.py    # メインプログラム
├── requirements.txt               # 依存関係
├── SETUP_GUIDE.md                 # このファイル
├── tts-key.json                   # ステップ3でダウンロードしたサービスアカウントキー
├── credentials.json               # ステップ4でダウンロードしたOAuth認証情報
└── slides/                        # 出力フォルダ（ステップ7の実行時に自動作成）
```

---

## ステップ6: 動作確認

###6.1 テスト用スライドの準備 💡

動作確認を行うため、事前に Google Slides でテスト用のプレゼンテーションを作成し、以下の準備を完了してください。

* **スライドの作成**: 複数スライドで構成されたプレゼンテーションを作成
* **スピーカーノートの入力**: 音声合成したい日本語テキストを各スライドのスピーカーノートに入力
* **共有設定**: 作成したスライドの共有設定を「**リンクを知っている全員が閲覧者**」（またはサービスアカウントに権限がある状態）に変更

### 6.2 プレゼンテーションIDの確認方法

プログラムの実行時に必要となる **プレゼンテーションID** は、Google Slides の URL 内に含まれています。以下の手順で確認してコピーしてください。

1. 作成したテスト用スライドをブラウザで開く
2. ブラウザのアドレスバーに表示されている URL を確認
3. URL の `d/` と `/edit` の間の文字列が **プレゼンテーションID**

**例: Google Slides URL**

```text
https://docs.google.com/presentation/d/1M_A-bC1234567890defGHIjklmNOpQR_S/edit#slide=id.p
```

**プレゼンテーションID**

```text
1M_A-bC1234567890defGHIjklmNOpQR_S
```

### 6.3 実行と初回認証

1. コマンドプロンプト/ターミナルで `Slides_to_Vids` フォルダに移動し、**仮想環境がアクティベート**されていることを確認

> ℹ️ 仮想環境がアクティベートされていると、プロンプトの先頭に `(slides-tts-env)` が表示されます。

2. 以下のコマンドを実行

```bash
python generate_tts_from_slides.py
```

3. プログラムが **URL または プレゼンテーションID** の入力を要求
4. コピーしておいた **プレゼンテーションID** を貼り付けて `Enter`
5. **初回のみ** ブラウザが自動起動し、認証画面が表示

   * Google アカウントでログインし、アプリの権限を承認
   * 認証完了後、ブラウザに `The authentication flow has completed. You may close this window.` と表示
6. 認証成功後、作業フォルダに **`token.pickle`** が自動作成され、音声合成処理が続行

### 6.4 出力ファイルの確認

処理完了後、`slides/` フォルダ（ステップ7の実行時に自動作成）内に、**スライドごとに生成された音声ファイル**が出力されていることを確認してください。

---

## トラブルシューティング

よくある問題と解決方法をまとめます。

### 1. 認証エラー

```
google.auth.exceptions.DefaultCredentialsError: Could not automatically determine credentials.
```

**解決**: `tts-key.json` が正しい場所（作業フォルダ直下）に配置されているか確認。

### 2. API 有効化エラー

```
googleapiclient.errors.HttpError: 403 Forbidden
```

**解決**:

* Google Cloud Console で必要な API が **有効化** されているか確認
* 対象プロジェクトが正しく **選択** されているか確認

### 3. スコープエラー

```
The user has not granted the app permission to access the resource
```

**解決**: OAuth 同意画面の設定を見直し、必要なスコープが追加されているか確認。

### 4. ファイルが見つからないエラー

```
FileNotFoundError: [Errno 2] No such file or directory: 'credentials.json'
```

**解決**: `credentials.json` が `Slides_to_Vids` フォルダに配置されているか確認。

---

## セキュリティ注意事項

* `tts-key.json` と `credentials.json` は **機密情報** です。
* これらのファイルを **Git リポジトリにコミットしない**でください。
* 社内共有時は、これらのファイルを **別途安全な方法**で配布してください。

---

## サポート

設定で問題が発生した場合は、以下を確認してください。

* Google Cloud Console の設定
* ファイルの配置場所
* Python 環境とパッケージのインストール状況
* エラーメッセージの詳細





