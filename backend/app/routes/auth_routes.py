from flask import Blueprint, request, jsonify
from app import bcrypt
from app.services import get_user_by_id, change_user_password, is_valid_password, is_valid_email, store_pending_user, send_verification_email, get_user_by_email, insert_user, get_pending_user_hashed_password, delete_pending_user, send_password_reset_email, used_reset_token, set_used_reset_token, update_user_password
from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity, jwt_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Validate email format
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400
    
    # Check if password meets the security requirements
    if not is_valid_password(password):
        return jsonify({"error": "Password must be at least 8 characters long, contain one uppercase letter, one lowercase letter, and one digit"}), 400

    if get_user_by_email(email):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    store_pending_user(email, hashed_password)
    send_verification_email(email)

    return jsonify({"message": "Verification email sent"}), 200


@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    try:        
        # Decode token to extract email
        decoded_token = decode_token(token)
        email = decoded_token.get("sub")
        
        hashed_password = get_pending_user_hashed_password(email)
        if not hashed_password:
            return jsonify({"error": "Invalid or expired token. Please sign up again."}), 400

        # Save user in the database
        insert_user(email, hashed_password)

        # Remove from Redis after successful verification
        delete_pending_user(email)

        return jsonify({"message": "Email verified successfully! You can now log in."}), 200

    except Exception as e:
        return jsonify({"error": "Invalid or expired token.", "details": str(e)}), 400
    
    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Check if user exists
    user = get_user_by_email(email)
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(
            identity=str(user.id),  # The unique identifier (user ID)
            additional_claims={"role": user.role}  # Include the role in the claims
        )

        # Return the access token
        return jsonify({
            "user_id": str(user.id),
            "access_token": access_token
        }), 200

    return jsonify(message="Invalid credentials"), 401


@auth_bp.route('/recover-password', methods=['POST'])
def recover_password():
    data = request.json
    email = data.get('email')
    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    send_password_reset_email(email)

    return jsonify({"message": "Password reset email sent"}), 200


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    reset_token = data.get('reset_token')
    new_password = data.get('new_password')

    try:
        if used_reset_token(reset_token):
            return jsonify({"error": "This reset link has already been used. Please request a new password reset email."}), 400
        
        if not is_valid_password(new_password):
            return jsonify({"error": "Password must be at least 8 characters long, contain one uppercase letter, one lowercase letter, and one digit"}), 400

        decoded_token = decode_token(reset_token)
        email = decoded_token.get("sub")
        user = get_user_by_email(email)

        if not user:
            return jsonify({"error": "Invalid or expired token"}), 400

        update_user_password(user, new_password)
        set_used_reset_token(reset_token)

        return jsonify({"message": "Password reset successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Invalid or expired token", "details": str(e)}), 400
    
@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.json
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    if not (current_password and new_password and confirm_password):
        return jsonify({"error": "Missing required fields"}), 400

    if new_password != confirm_password:
        return jsonify({"error": "New passwords do not match"}), 400

    # Get the current user ID from the JWT token.
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        change_user_password(user, current_password, new_password)
        return jsonify({"message": "Password changed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400