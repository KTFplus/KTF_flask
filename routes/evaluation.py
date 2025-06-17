from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import requests, tempfile, os
from utils.error_response import error_response
from config import EVAL_SERVER_URL

eval_bp = Blueprint('evaluation', __name__)

@eval_bp.route("/api/pronunciation-evaluate", methods=["POST"])
def evaluate_pronunciation():
    try:
        audio_file = request.files.get("audio")
        sentence_id = request.form.get("sentenceId")
        user_id = request.form.get("userId", "test-users")

        if not audio_file or not sentence_id:
            return error_response("MISSING_FIELDS", "필수 필드(audio, sentenceId)가 누락되었습니다."), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio_file.save(tmp.name)
            files = {"audio": open(tmp.name, "rb")}
            data = {"sentenceId": sentence_id, "userId": user_id}
            response = requests.post(EVAL_SERVER_URL, files=files, data=data)
            os.unlink(tmp.name)

        return jsonify(response.json())

    except Exception as e:
        return error_response("EVAL_FAILED", "발음 평가에 실패했습니다.", {"exception": str(e)}), 500