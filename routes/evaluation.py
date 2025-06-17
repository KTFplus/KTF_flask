from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import requests, tempfile, os

# ⛔ 기존: from config import EVAL_SERVER_URL
# ✅ 변경: 직접 변수 선언
EVAL_SERVER_URL = "https://wise-positively-octopus.ngrok-free.app/api/analyze-audio"

eval_bp = Blueprint('evaluation', __name__)

@eval_bp.route("/pronunciation-evaluate", methods=["POST"])
def evaluate_pronunciation():
    try:
        print("📟 request.form:", request.form)
        print("📂 request.files:", request.files)

        audio_file = request.files.get("audio")
        sentenceId = request.form.get("sentenceId")
        userId = request.form.get("userId", "test-users")

        print("✅ sentenceId:", sentenceId)
        print("✅ audio_file:", audio_file)

        if not audio_file or not sentenceId:
            return jsonify({
                "error": "MISSING_FIELDS",
                "message": "필수 필드(audio, sentenceId)가 누락되었습니다."
            }), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio_file.save(tmp.name)
            files = {"audio": open(tmp.name, "rb")}
            data = {"sentenceId": sentenceId, "userId": userId}
            print("Sending to EVAL_SERVER_URL:", EVAL_SERVER_URL)
            print("POST data:", data)
            response = requests.post(EVAL_SERVER_URL, files=files, data=data)
            os.unlink(tmp.name)

        print("Received status code:", response.status_code)
        print("Received content:", response.text)

        if response.status_code != 200:
            return jsonify({
                "error": "DOWNSTREAM_ERROR",
                "message": "발음 평가 서버에서 200이 아닙니다.",
                "status_code": response.status_code,
                "response": response.text
            }), response.status_code

        return jsonify(response.json())

    except Exception as e:
        print("❌ Exception:", str(e))
        return jsonify({
            "error": "EVAL_FAILED",
            "message": "발음 평가에 실패했습니다.",
            "exception": str(e)
        }), 500
