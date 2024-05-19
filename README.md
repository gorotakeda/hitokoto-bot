# hitokoto-bot

## 環境構築
- git clone
- docker-compose build
- docker-compose up

## デプロイ手順
- brew tap heroku/brew && brew install heroku
- heroku login
- heroku create news-hitokoto-bot
- heroku container:login
- heroku config:set FLASK_APP=app/app.py FLASK_ENV=production -a news-hitokoto-bot
- heroku config:set APP_SECRET_KEY='abcd1234' -a news-hitokoto-bot
- heroku config:set NEWS_API_KEY='your_news_api_key' -a news-hitokoto-bot
- heroku config:set OPENAI_API_KEY='your_openai_api_key' -a news-hitokoto-bot
- docker build --platform linux/amd64 -t registry.heroku.com/news-hitokoto-bot/web .
- docker push registry.heroku.com/news-hitokoto-bot/web
- heroku container:release web -a news-hitokoto-bot
- heroku restart -a news-hitokoto-bot
- heroku open -a news-hitokoto-bot
  
## URL
https://news-hitokoto-bot-f3b4988ed870.herokuapp.com/
