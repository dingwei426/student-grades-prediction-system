from flask import Blueprint, request, jsonify, current_app
from app.services import get_default_field_by_user_id, set_default_field, get_user_by_id, generate_prediction, get_prediction_list_user_id, get_prediction_by_id, update_prediction_name_service, delete_prediction_service
from flask_jwt_extended import get_jwt_identity, jwt_required

prediction_bp = Blueprint("prediction", __name__, url_prefix="/prediction")

@prediction_bp.route('/get_default_field', methods=['GET'])
@jwt_required()
def get_default_field():
    try:
        user_id = get_jwt_identity()

        user = get_user_by_id(user_id)

        if not user:
            return jsonify(message="User not found"), 404  # Ensure the user exists
        
        if user.role != 'user':
            return jsonify(message="Access denied. Users only."), 403

        result = get_default_field_by_user_id(user_id)

        if not result:
            return jsonify({}), 200

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@prediction_bp.route('/update_default_field', methods=['POST'])
@jwt_required()
def update_default_field():
    try:
        user_id = get_jwt_identity()
        user = get_user_by_id(user_id)

        if not user:
            return jsonify(message="User not found"), 404  # Ensure the user exists
        
        if user.role != 'user':
            return jsonify(message="Access denied. Users only."), 403

        form_data = request.get_json()
        print("Form Data:", form_data)  # Debugging

        if not form_data:
            return jsonify({'error': 'No data provided'}), 400

        # Call the helper function to update or insert the data
        record_id = set_default_field(form_data, user_id)

        return jsonify({
            'message': 'Default field updated successfully',
            'record_id': record_id
        }), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500

@prediction_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    user_id = get_jwt_identity()

    user = get_user_by_id(user_id)

    if not user:
        return jsonify(message="User not found"), 404  # Ensure the user exists
    
    if user.role != 'user':
        return jsonify(message="Access denied. Users only."), 403

    data = request.json
    print("selected_subjects", data.get('selected_subjects'))  # Debugging

    model_type = data.get('model_type')
    selected_subjects = data.get('selected_subjects')
    if model_type not in {'lgbm_4', 'rf_4', 'lgbm_9', 'rf_9'}:
        return jsonify(message="Invalid model type"), 400
    
    prediction_id = generate_prediction(data.get('form_data'), user_id, model_type, selected_subjects)   
    return jsonify(prediction_id=prediction_id), 200

@prediction_bp.route('/get_predictions', methods=['GET'])
@jwt_required()
def get_predictions():
    user_id = get_jwt_identity()

    user = get_user_by_id(user_id)

    if not user:
        return jsonify(message="User not found"), 404  # Ensure the user exists
    
    if user.role != 'user':
        return jsonify(message="Access denied. Users only."), 403

    predictions = get_prediction_list_user_id(user_id)

    if not predictions:
        return jsonify({"message": "No predictions found for this user."}), 404

    return jsonify({"predictions": predictions}), 200

@prediction_bp.route('/get_prediction', methods=['GET'])
@jwt_required()
def get_prediction():
    prediction_id = request.args.get('prediction_id', type=int)

    if not prediction_id:
        return jsonify({"error": "prediction_id is required as a query parameter."}), 400

    prediction = get_prediction_by_id(prediction_id)

    if not prediction:
        return jsonify({"message": "No predictions found for this user."}), 404

    return jsonify({"prediction": prediction}), 200

@prediction_bp.route('/update_prediction_name/<int:prediction_id>', methods=['PUT'])
@jwt_required()
def update_prediction_name(prediction_id):
    data = request.get_json()
    new_name = data.get('new_name')
    response, status_code = update_prediction_name_service(prediction_id, new_name)
    return jsonify(response), status_code

@prediction_bp.route('/delete_prediction/<int:prediction_id>', methods=['DELETE'])
@jwt_required()
def delete_prediction(prediction_id):
    response, status_code = delete_prediction_service(prediction_id)
    return jsonify(response), status_code
