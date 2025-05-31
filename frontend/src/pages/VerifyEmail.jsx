import React, { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import { verifyEmail } from "../services/authServices";
import PageHeader from "../components/PageHeader";

const VerifyEmail = () => {
  const { token } = useParams();
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const hasFetched = useRef(false);

  useEffect(() => {
    if (hasFetched.current) return;
    hasFetched.current = true;

    const verify = async () => {
      setLoading(true);

      try {
        const response = await verifyEmail(token);
        setSuccess(response.data.message);
        setError("");
      } catch (err) {
        setError(
          err.response?.data?.error || "An error occurred during verification."
        );
        setSuccess("");
      } finally {
        setLoading(false);
      }
    };

    verify();
  }, [token]);

  return (
    <div className="container">
      <div style={{ marginTop: "5%" }}></div>
      <PageHeader
        title="Student Grades and CGPA Prediction System"
        color="#0a4279"
      />
      <div className="login-box">
        <h2 className="login-header">Email Verification</h2>
        {loading && <p className="loading">Verifying...</p>}
        {success && <p className="success-message">{success}</p>}
        {error && <p className="error-message">{error}</p>}
        <div className="small-text">
          <p>
            Back to login. <a href="../login">Login</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default VerifyEmail;
