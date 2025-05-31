import React, { useState, useEffect } from "react";
import { login } from "../services/authServices";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import PageHeader from "../components/PageHeader";
import LoginForm from "../components/LoginForm";
import "../assets/styles.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token) {
      try {
        const decoded = jwtDecode(token);
        const userRole = decoded.role;
        navigate(userRole === "admin" ? "/admin" : "/home");
      } catch (error) {
        console.error("Invalid token:", error);
      }
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    if (loading) return;
    setLoading(true);

    try {
      const response = await login(email, password);
      const { access_token } = response.data;
      localStorage.setItem("access_token", access_token);
      const decoded = jwtDecode(access_token);
      navigate(decoded.role === "admin" ? "/admin" : "/home");
    } catch (err) {
      setErrorMessage("Invalid credentials");
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
      <LoginForm
        email={email}
        password={password}
        setEmail={setEmail}
        setPassword={setPassword}
        showPassword={showPassword}
        setShowPassword={setShowPassword}
        handleLogin={handleLogin}
        errorMessage={errorMessage}
        loading={loading}
      />
    </div>
  );
};

export default Login;
