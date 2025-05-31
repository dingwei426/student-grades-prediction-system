from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services import (
    get_most_used_model,
    get_primary_language_distribution,
    get_average_revision_time,
    get_cgpa_comparison,
    get_subject_grade_distribution,
    get_qualification_type_distribution
)

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/most_used_models", methods=["GET"])
@jwt_required()
def most_used_models():
    return jsonify(get_most_used_model())


@dashboard_bp.route("/primary_language_distribution", methods=["GET"])
@jwt_required()
def primary_language_distribution():
    return jsonify(get_primary_language_distribution())


@dashboard_bp.route("/average_revision_time", methods=["GET"])
@jwt_required()
def average_revision_time():
    return jsonify({
        "average_revision_time": get_average_revision_time()
    })


@dashboard_bp.route("/cgpa_comparison", methods=["GET"])
@jwt_required()
def cgpa_comparison():
    return jsonify(get_cgpa_comparison())


@dashboard_bp.route("/subject_grade_distribution", methods=["GET"])
@jwt_required()
def subject_grade_distribution():
    subject = request.args.get("subject")
    if not subject:
        return jsonify({"error": "Subject parameter is required"}), 400

    return jsonify(get_subject_grade_distribution(subject))


@dashboard_bp.route("/qualification_distribution", methods=["GET"])
@jwt_required()
def qualification_type_distribution():
    try:
        result = get_qualification_type_distribution()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500