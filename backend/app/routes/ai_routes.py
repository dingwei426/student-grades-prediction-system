from flask import Blueprint, request, jsonify, current_app
from app.services import (openrouter, get_ai_recommendation, save_ai_recommendation, get_user_by_id)
from flask_jwt_extended import get_jwt_identity, jwt_required
import json
ai_bp = Blueprint("ai", __name__, url_prefix="/ai")

@ai_bp.route('/openrouter_recommendation', methods=['GET'])
@jwt_required()
def openrouter_recommendation():
     # 1) Auth & role check
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.role != "user":
        return jsonify({"error": "Access denied"}), 403

    pid = request.args.get("prediction_id", type=int)
    if not pid:
        return jsonify({"error": "prediction_id is required"}), 400

    try:
        ai_response = openrouter(pid)
        # ai_response is the tuple (Response, status_code)
        response_obj = ai_response[0]

        # get JSON string
        response_text = response_obj.get_data(as_text=True)

        # parse JSON
        response_json = json.loads(response_text)
        suggestion = response_json['choices'][0]['message']['content']
        save_ai_recommendation(pid, suggestion)
    except Exception as e:
        return (
            jsonify({"error": "AI service failed", "details": str(e)}),
            502,
        )
    return jsonify({"response": suggestion}), 200
    
@ai_bp.route('/retrieve_suggestion', methods=['GET'])
@jwt_required()
def retrieve_suggestion():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.role != "user":
        return jsonify({"error": "Access denied"}), 403

    pid = request.args.get("prediction_id", type=int)
    if not pid:
        return jsonify({"error": "prediction_id is required"}), 400

    try:
        suggestion = get_ai_recommendation(pid)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404

    if suggestion:
        return jsonify({"response": suggestion}), 200
    else:
        return jsonify({"message": "No suggestion found for this prediction."}), 404

# @ai_bp.route('/generate_suggestion', methods=['GET'])
# @jwt_required()
# def generate_suggestion():
#     # 1) Auth & role check
#     user_id = get_jwt_identity()
#     user = get_user_by_id(user_id)

#     if not user:
#         return jsonify({"error": "User not found"}), 404
#     if user.role != "user":
#         return jsonify({"error": "Access denied"}), 403

#     pid = request.args.get("prediction_id", type=int)
#     if not pid:
#         return jsonify({"error": "prediction_id is required"}), 400

#     try:
#         question = get_ai_input(pid)
#     except ValueError as ve:
#         return jsonify({"error": str(ve)}), 404

#     try:
#         ai_response = call_ai_model(question)
#     except Exception as e:
#         return (
#             jsonify({"error": "AI service failed", "details": str(e)}),
#             502,
#         )

#     try:
#         save_ai_recommendation(pid, ai_response)
#     except ValueError as ve:
#         return jsonify({"error": str(ve)}), 404

#     return jsonify({"response": ai_response}), 200