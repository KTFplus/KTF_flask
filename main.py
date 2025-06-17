from flask import Flask
from flask_cors import CORS
from routes.audio import audio_bp
from routes.evaluation import eval_bp

app = Flask(__name__)
CORS(app)

# 라우트 등록
app.register_blueprint(audio_bp)
app.register_blueprint(eval_bp)

if __name__ == "__main__":
    app.run(port=5001, debug=True)