from flask import Blueprint, request, jsonify
import requests

eval_bp = Blueprint("eval", __name__)
EVAL_SERVER_URL = "https://wise-positively-octopus.ngrok-free.app/api/analyze-audio"  # Colab

@eval_bp.route("/pronunciation-evaluate", methods=["POST"])
def forward_evaluation():
    try:
        # ✅ 필수 필드 검증
        if 'audio' not in request.files or 'sentenceId' not in request.form:
            return jsonify({"error": "Missing required fields"}), 400

        # ✅ 파일 및 폼 데이터 준비
        audio_file = request.files['audio']
        sentence_id = request.form['sentenceId']
        user_id = request.form.get('userId', 'anonymous')

        print("🎯 프록시에서 Colab으로 전송:")
        print("  🔊 audio filename:", audio_file.filename)
        print("  📄 sentenceId:", sentence_id)
        print("  👤 userId:", user_id)

        # ✅ requests용 데이터 구성
        files = {
            'audio': (audio_file.filename, audio_file.stream, audio_file.mimetype)
        }
        data = {
            'sentenceId': sentence_id,
            'userId': user_id
        }

        # ✅ Colab 서버로 요청 전송
        response = requests.post(EVAL_SERVER_URL, files=files, data=data)

        # ✅ Colab 응답 그대로 반환
        return (response.content, response.status_code, response.headers.items())

    except Exception as e:
        print("🔥 프록시 오류:", str(e))
        return jsonify({"error": str(e)}), 500
