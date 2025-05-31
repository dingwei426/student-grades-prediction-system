import React, { useState } from "react";
import { recoverPassword } from "../services/authServices";
import PageHeader from "../components/PageHeader";
import InputWithLabel from "../components/InputWithLabel";
import LongButton from "../components/LongButton";
import "../assets/styles.css";

const RecoverPassword = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await recoverPassword(email);
      setMessage("Password reset link sent to your email.");
    } catch (error) {
      setMessage("User not found.");
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
        <p className="login-header">Recover Password</p>

        {/* Email Input Field */}
        <InputWithLabel
          label="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
        />

        {/* Submit Button */}
        <LongButton
          text={loading ? "Sending..." : "Send Reset Link"}
          type="submit"
          disabled={loading}
        />

        {/* Display the message */}
        {message && (
          <p
            className={
              message.includes("not") ? "error-message" : "success-message"
            }
          >
            {message}
          </p>
        )}
        <div className="small-text" style={{ marginTop: "0px" }}>
          <p>
            Back to login. <a href="./login">Login</a>
          </p>
        </div>
      </form>
    </div>
  );
};

export default RecoverPassword;
