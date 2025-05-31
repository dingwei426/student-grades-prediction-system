import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { resetPassword } from "../services/authServices";
import PageHeader from "../components/PageHeader";
import InputWithLabel from "../components/InputWithLabel";
import LongButton from "../components/LongButton";

const ResetPassword = () => {
  const { reset_token } = useParams();
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading) return;
    setLoading(true);

    if (password !== confirmPassword) {
      setErrorMessage("Passwords do not match.");
      setLoading(false);
      return;
    }

    try {
      await resetPassword(reset_token, password);
      setSuccessMessage("Password reset successfully! Redirecting to login...");
      setErrorMessage("");
      setTimeout(() => navigate("/login"), 3000);
    } catch (error) {
      setErrorMessage(
        error.response?.data?.error || "Error: Could not reset password."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div style={{ marginTop: "5%" }}></div>
      <PageHeader
        title="Student Grades and CGPA Prediction System"
        color="#0a4279"
      />
      <form onSubmit={handleSubmit} className="login-box">
        <h2 className="login-header">Reset Your Password</h2>

        <InputWithLabel
          label="New Password"
          type={showPassword ? "text" : "password"}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
          errorMessage={""}
        />

        <InputWithLabel
          label="Confirm Password"
          type={showPassword ? "text" : "password"}
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Enter your password"
          errorMessage={errorMessage}
        />

        <div className="options">
          <label>
            <input
              type="checkbox"
              checked={showPassword}
              onChange={() => setShowPassword(!showPassword)}
            />
            Show Password
          </label>
        </div>

        <LongButton
          text="Reset Password"
          type="submit"
          disabled={loading || !password || !confirmPassword}
        />
        <div className="small-text">
          <p>
            Back to Login. <a href="../login">Login</a>
          </p>
        </div>
        {successMessage && <p className="success-message">{successMessage}</p>}
      </form>
    </div>
  );
};

export default ResetPassword;
