from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import requests, tempfile, os
from utils.error_response import error_response
from config import ASR_SERVER_URL

audio_bp = Blueprint('audio', __name__)

@audio_bp.route("/upload-audio", methods=["POST"])
def upload_audio():
    try:
        audio_file = request.files.get("audio")
        user_id = request.form.get("userId", "test-users")

        if not audio_file:
            return error_response("NO_FILE", "오디오 파일이 없습니다."), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio_file.save(tmp.name)
            files = {"audio": open(tmp.name, "rb")}
            data = {"userId": user_id}
            response = requests.post(ASR_SERVER_URL, files=files, data=data, verify=False)
            os.unlink(tmp.name)  # 처리 후 파일 삭제

        return jsonify(response.json())

    except Exception as e:
        import traceback
        traceback.print_exc()
        return error_response("ASR_FAILED", "음성 인식에 실패했습니다.", {"exception": str(e)}), 500