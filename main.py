from flask import Flask
from flask_cors import CORS
from routes.audio import audio_bp
from routes.evaluation import eval_bp
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

# 라우트 등록
app.register_blueprint(audio_bp)
app.register_blueprint(eval_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)