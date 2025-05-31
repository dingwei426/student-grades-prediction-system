from flask import jsonify, current_app
from app import db, bcrypt, mail
from app.models import User
from flask_mail import Message
from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask import render_template_string
import re

def get_redis_client():
    """Retrieve Redis client from Flask app config."""
    return current_app.config["SESSION_REDIS"]

def is_valid_password(password):
    """Checks if the password meets the criteria:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    """
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password))

def is_valid_email(email):
    """Checks if the email is in a valid format."""
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(EMAIL_REGEX, email) is not None

def store_pending_user(email, hashed_password):
    redis_client = get_redis_client()
    redis_client.setex(f"pending_user:{email}", 3600, hashed_password)


def get_pending_user_hashed_password(email):
    redis_client = get_redis_client()
    return redis_client.get(f"pending_user:{email}")


def delete_pending_user(email):
    redis_client = get_redis_client()
    redis_client.delete(f"pending_user:{email}")


def send_verification_email(recipient_email):
    verification_token = create_access_token(identity=recipient_email, expires_delta=timedelta(hours=1))
    verify_link = f"http://localhost:3000/verify-email/{verification_token}"

    html_content = render_template_string("""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f6f8fb; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
          <h2 style="color: #2f527a;">Verify Your Email</h2>
          <p>Hello,</p>
          <p>Thank you for signing up! Please verify your email address by clicking the button below:</p>
          <div style="text-align: center; margin: 30px 0;">
            <a href="{{ verify_link }}" style="background-color: #2f527a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Verify Email</a>
          </div>
          <p>If the button doesn't work, copy and paste the following link into your browser:</p>
          <p style="word-break: break-all;"><a href="{{ verify_link }}">{{ verify_link }}</a></p>
          <p style="color: #999;">This link will expire in 1 hour.</p>
          <p>Student Prediction System<br/>The Support Team</p>
        </div>
      </body>
    </html>
    """, verify_link=verify_link)

    msg = Message(
        subject="Verify Your Email",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[recipient_email],
        html=html_content  # Set HTML content
    )

    mail.send(msg)


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def insert_user(email, hashed_password):
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()


# def send_password_reset_email(email):
#     reset_token = create_access_token(identity=email, expires_delta=timedelta(minutes=10))

#     msg = Message(
#         'Password Reset Request',
#         sender=current_app.config['MAIL_DEFAULT_SENDER'],
#         recipients=[email]
#     )
#     msg.body = f"To reset your password, use the following link:\n\n" \
#                f"http://localhost:3001/reset-password/{reset_token}\n\n" \
#                f"This link will expire in 10 minutes."

#     mail.send(msg)

#     return jsonify({"message": "Password reset email sent"}), 200


def send_password_reset_email(email):
    reset_token = create_access_token(identity=email, expires_delta=timedelta(minutes=10))
    reset_link = f"http://localhost:3000/reset-password/{reset_token}"

    html_content = render_template_string("""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f6f8fb; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
          <h2 style="color: #2f527a;">Password Reset Request</h2>
          <p>Hello,</p>
          <p>We received a request to reset your password. You can reset it by clicking the button below:</p>
          <div style="text-align: center; margin: 30px 0;">
            <a href="{{ reset_link }}" style="background-color: #2f527a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Reset Password</a>
          </div>
          <p>If the button above doesn’t work, you can also copy and paste this link into your browser:</p>
          <p style="word-break: break-all;"><a href="{{ reset_link }}">{{ reset_link }}</a></p>
          <p style="color: #999;">This link will expire in 10 minutes.</p>
          <p>Student Prediction System<br/>The Support Team</p>
        </div>
      </body>
    </html>
    """, reset_link=reset_link)

    msg = Message(
        subject="Password Reset Request",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[email],
        html=html_content  # HTML content
    )

    mail.send(msg)
    return jsonify({"message": "Password reset email sent"}), 200


def used_reset_token(reset_token):
    redis_client = get_redis_client()
    return bool(redis_client.get(f"used_token:{reset_token}"))


def set_used_reset_token(reset_token):
    redis_client = get_redis_client()
    redis_client.setex(f"used_token:{reset_token}", 600, "used")


def update_user_password(user, new_password):
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = hashed_password
    db.session.commit()


def change_user_password(user, current_password, new_password):
    # Check if the provided current password matches the user's stored password.
    if not bcrypt.check_password_hash(user.password, current_password):
        raise Exception("Current password is incorrect")

    # Check if the new password meets the security requirements.
    if not is_valid_password(new_password):
        raise Exception(
            "New password must be at least 8 characters long, contain one uppercase letter, one lowercase letter, and one digit"
        )

    # Hash the new password and update the user record.
    hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
    user.password = hashed_password
    db.session.commit()