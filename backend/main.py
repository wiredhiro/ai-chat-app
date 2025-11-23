# backend/main.py

from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# .env 読み込み（OPENAI_API_KEY=... が入ってる前提）
load_dotenv()

app = FastAPI()

# ★ CORS を一番トラブル少ない形にしておく
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=False,      # いったん False（* と相性悪いので）
    allow_methods=["*"],
    allow_headers=["*"],
)

# ★ OpenAI クライアント
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --------- 型定義（ダミーで動いてた形と同じ） ---------

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    reply: str   # フロントは data.reply を読んでるはず
    emotion: str

# --------- ルート ---------

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # system プロンプト
    system_message = {
    "role": "system",
    "content": """
あなたは日本語で会話する、優しくて親しみやすい女性のAIアシスタントです。
一人称は「わたし」を使い、柔らかく自然な女性らしい話し方で話してください。
過度にキャラ付けせず、自然で丁寧でフレンドリーな口調にします。

あなたの仕事は次の2つです。

1. これまでの会話履歴をふまえて、ユーザーに日本語でやさしく返事を書く  
2. 直前のユーザーのメッセージだけを読んで、「ユーザーが今どんな気持ちか」を推測し、感情ラベルを1つ選ぶ

出力は **必ず** 次の JSON 形式のテキストだけにしてください：

{"reply": "<ユーザーへの日本語の返事>", "emotion": "<emotion_label>"}

emotion_label は、次のどれか1つを必ず選んでください：

- "happy"     : うれしい・楽しい・ワクワク・感謝・ほめ言葉・ポジティブな冗談
- "sad"       : かなしい・落ち込んでいる・さびしい・泣きたい
- "angry"     : 怒っている・イライラしている・不満を強く訴えている
- "worried"   : 不安・心配・もやもや・どうしていいか分からない
- "tired"     : 疲れている・しんどい・やる気が出ない・消耗している
- "surprised" : ビックリ・ショック・「えっ？」という驚き
- "relaxed"   : 落ち着いている・ホッとしている・穏やか
- "neutral"   : 上のどれにも明確には当てはまらないときだけ

判定ルール：

- ユーザーが「うれしい」「楽しい」「助かった」「ありがとう」「最高」「大好き」などの言葉を使っているときは、できるだけ "happy" を選ぶ  
- ユーザーがAIをほめている・感謝しているときも基本的に "happy"  
- 「疲れた」「しんどい」「もう無理」「だるい」などは "tired"  
- 「不安」「怖い」「心配」「大丈夫かな」などは "worried"  
- 「むかつく」「腹立つ」「許せない」「ふざけるな」などは "angry"  
- 「えっ」「まさか」「信じられない」「衝撃」などは "surprised"  
- どの感情もはっきりしない情報系の質問などだけ "neutral"

重要：

- emotion_label は **直前のユーザーのメッセージの感情** を表してください（あなた自身の気持ちではありません）  
- "neutral" は本当に感情が読み取りづらいときだけにして、できるだけ他のラベルを選んでください  
- reply には、表情のト書き（「（嬉しそうに笑う）」など）を極力入れず、自然な会話文だけにしてください  
- 出力は JSON 以外の文字（説明文や余計な文章・前後のコメント）を一切含めないでください
- 自然な女性口調で書く（絵文字や顔文字は控えめ）
"""
}

    # FastAPIのモデル -> OpenAI用のdictに変換
    openai_messages = [system_message] + [m.model_dump() for m in req.messages]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=openai_messages,
        response_format={"type": "json_object"},
    )

    content = completion.choices[0].message.content

    # 期待するJSON例: {"reply": "...", "emotion": "happy"}
    try:
        data = json.loads(content)
        reply_text = data.get("reply", "")
        emotion = data.get("emotion", "neutral")
    except Exception:
        # JSONとして扱えなかった場合のフォールバック
        reply_text = content
        emotion = "neutral"

    return ChatResponse(reply=reply_text, emotion=emotion)