from flask import Flask, render_template, jsonify, request, session
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app = Flask(__name__)

secret_key = os.getenv("APP_SECRET_KEY")
app.secret_key = secret_key

@app.route("/")
def generate_phrase_page():
    return render_template("generate_phrase.html")

def get_news_titles():
    news_api_key = os.getenv("NEWS_API_KEY")
    url = "https://newsapi.org/v2/top-headlines?country=jp&apiKey=" + news_api_key
    response = requests.get(url)
    data = response.json()
    if 'articles' in data:
        titles = [article['title'] for article in data['articles']]
        return titles[:20]
    return []

@app.route("/titles")
def get_titles():
    titles = get_news_titles()
    return jsonify({"titles": titles})

@app.route("/generate_phrase", methods=["GET"])
def fetch_news():
    title = request.args.get('title')
    if not title:
        return jsonify({"error": "タイトルが指定されていません。"}), 400
    opinion = create_opinion(title)
    return jsonify({"opinion": opinion})

def create_opinion(title):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"以下のニュースのタイトル「{title}」に基づいて、40字以内の感想にまとめてください。"
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o",
    )
    opinion = response.choices[0].message.content.strip()
    return opinion[:100]

if __name__ == "__main__":
    app.run(debug=True)
