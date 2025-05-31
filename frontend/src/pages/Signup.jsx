import React, { useState } from "react";
import { signup } from "../services/authServices";
import PageHeader from "../components/PageHeader";
import SignupForm from "../components/SignupForm";

const Signup = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault();
    if (loading) return;
    setLoading(true);

    try {
      await signup(email, password);
      setSuccessMessage(
        "Signup successful! A verification email has been sent."
      );
      setErrorMessage("");
      setEmail("");
      setPassword("");
    } catch (err) {
      setErrorMessage(
        err.response?.data?.error || "An error occurred. Please try again."
      );
      setSuccessMessage("");
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

      <SignupForm
        email={email}
        password={password}
        setEmail={setEmail}
        setPassword={setPassword}
        showPassword={showPassword}
        setShowPassword={setShowPassword}
        handleSignup={handleSignup}
        errorMessage={errorMessage}
        successMessage={successMessage}
        loading={loading}
      />
    </div>
  );
};

export default Signup;
