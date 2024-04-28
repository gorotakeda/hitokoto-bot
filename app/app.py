from flask import Flask, render_template, jsonify, request, session
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import random

load_dotenv()
app = Flask(__name__)

secret_key = os.getenv("APP_SECRET_KEY")
app.secret_key = secret_key

@app.route("/")
def generate_phrase_page():
    return render_template("generate_phrase.html")

def fetch_news_and_generate_phrase(keyword):
    news_api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q={keyword}&sortBy=publishedAt&apiKey={news_api_key}"
    response = requests.get(url)
    data = response.json()

    if 'articles' not in data or not data['articles']:
        return None, "指定されたキーワードのニュースはありません。"

    random_article = random.choice(data["articles"])
    title = random_article["title"][:60]  # タイトルを取得
    description = random_article.get("description", "")  # 記事の説明（本文）を取得
    full_text = f"{title}\n{description}"  # タイトルと説明を組み合わせる
    return full_text, None

def generate_opinion_from_article(article_text):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # プロンプトの設定
    prompt = f"以下のニュース記事のタイトルと記事内容に基づいて、40字以内の感想を教えてください:\n{article_text}"

    # テキスト生成を行う
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )
    opinion = response.choices[0].message.content.strip()
    return opinion[:100]  # 必要に応じて文字数制限を調整

@app.route("/generate_phrase", methods=["GET"])
def fetch_news():
    keyword = request.args.get('keyword', '')
    article_text, error_message = fetch_news_and_generate_phrase(keyword)
    if error_message:
        return jsonify({"error": error_message}), 404
    opinion = generate_opinion_from_article(article_text)
    return jsonify({"opinion": opinion})
