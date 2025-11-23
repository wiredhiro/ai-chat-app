# AI Chat App

Python（FastAPI） + React（Vite + TypeScript）で構築した、感情推定付きチャットアプリです。  
ユーザーの発言内容から感情を推定し、AI 側のアバターが `happy / sad / angry / worried / neutral` などの表情に変化します。

---

## 🌟 機能

- 🎭 **OpenAI API を使った感情推定**
- 🤖 **AI が返答ごとにアバター画像を変更**
- 💬 **チャット UI（バブル・右左配置・タイピングインジケータ）**
- 🧪 **ローカル環境で完結**

---

## 📂 ディレクトリ構成

ai-chat-app/
├── backend/ # FastAPI（Python）
│ ├── main.py
│ ├── requirements.txt
│ └── sample.env # コピーして .env を作成
└── frontend/ # React + Vite
├── src/
├── public/avatars/ # 表情アイコン画像
└── package.json

---

## 🔧 **バックエンド（FastAPI）セットアップ**

### **① backend へ移動**

```bash
cd backend

② 仮想環境作成

python3 -m venv .venv

③ 仮想環境を有効化

Mac / Linux：

source .venv/bin/activate

Windows：

.\.venv\Scripts\activate

④ 必要なパッケージをインストール

pip install -r requirements.txt

⑤ .env を作成（サンプルをコピー）

cp sample.env .env

.env を編集：

OPENAI_API_KEY="あなたのAPIキー"

⑥ サーバー起動

uvicorn main:app --reload --port 8000


⸻

🖥 フロントエンド（React + Vite）セットアップ

① frontend へ移動

cd frontend

② 依存インストール

npm install

③ 開発サーバー起動

npm run dev

→ ブラウザで開く：

http://localhost:5173


⸻

🔗 API 接続について

フロントエンドは以下のURLをコールします：

http://localhost:8000/chat

両方同時に起動しておく必要があります：

サービス	コマンド	URL
Backend	uvicorn main:app --reload --port 8000	http://localhost:8000
Frontend	npm run dev	http://localhost:5173


⸻

🔐 環境変数（含めないもの）

リポジトリには含めません：

ファイル	理由
.env	APIキーが含まれるため
.venv/	個別環境で異なるため
node_modules/	再生成可能
__pycache__/	キャッシュ

.gitignore により自動除外しています。

⸻

📜 ライセンス / 利用について
	•	コードは自由に改変・利用可能（学習・個人利用OK）
	•	OpenAI API の利用規約には従ってください
	•	キャラクター画像はあなた自身の素材に交換可能

⸻

👤 作者

Hiro
フロントエンド

⸻
```
