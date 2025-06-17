from flask import jsonify

def error_response(code, message, details=None):
    return jsonify({
        "error": {
            "code": code,
            "message": message,
            "details": details or {}
        }
    })