FROM python:3

WORKDIR /app

COPY . /app

# pipのアップグレード
RUN pip install --upgrade pip

# requirements.txtを参照してパッケージをインストール
RUN pip install -r requirements.txt

CMD ["/bin/sh", "-c", "if [ \"$FLASK_ENV\" = \"development\" ]; then flask run --reload --host=0.0.0.0 --port=$PORT; else gunicorn app.app:app --bind 0.0.0.0:$PORT; fi"]
