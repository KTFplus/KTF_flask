from flask import Blueprint, request, jsonify
import requests
import tempfile
import os

eval_bp = Blueprint("eval", __name__)
EVAL_SERVER_URL = "https://wise-positively-octopus.ngrok-free.app/api/analyze-audio"  # Colab

@eval_bp.route("/pronunciation-evaluate", methods=["POST"])
def forward_evaluation():
    try:
        audio = request.files.get("audio")
        sentence_id = request.form.get("sentenceId")
        user_id = request.form.get("userId", "test-user")

        # ✅ 필수 필드 확인
        if not audio or not sentence_id:
            return jsonify({"error": "Missing required fields"}), 400

        print("🎯 프록시에서 Colab으로 전송:")
        print("  🔊 audio filename:", audio.filename)
        print("  📄 sentenceId:", sentence_id)
        print("  👤 userId:", user_id)

        # ✅ 오디오 파일을 임시 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio.save(tmp.name)
            files = {"audio": open(tmp.name, "rb")}
            data = {
                "sentenceId": sentence_id,
                "userId": user_id
            }

            # ✅ Colab으로 요청 전송
            response = requests.post(EVAL_SERVER_URL, files=files, data=data, verify=False)
            os.unlink(tmp.name)  # 파일 삭제

        return jsonify(response.json()), response.status_code

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
