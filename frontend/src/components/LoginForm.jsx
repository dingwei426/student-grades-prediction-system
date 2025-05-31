import React from "react";
import InputWithLabel from "./InputWithLabel";
import LongButton from "./LongButton";

const LoginForm = ({
  email,
  password,
  setEmail,
  setPassword,
  showPassword,
  setShowPassword,
  handleLogin,
  errorMessage,
  loading,
}) => {
  return (
    <form onSubmit={handleLogin} className="login-box">
      <p className="login-header">Login Form</p>

      <InputWithLabel
        label="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
      />
      <InputWithLabel
        label="Password"
        type={showPassword ? "text" : "password"}
        value={password}
        onChange={(e) => setPassword(e.target.value)}
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
        <a href="/recover-password">Forgot Password?</a>
      </div>

      <LongButton
        text="Login"
        type="submit"
        disabled={loading || !email || !password}
      />

      <div className="small-text">
        <p>
          Don't have an account? <a href="./signup">Sign Up</a>
        </p>
      </div>
    </form>
  );
};

export default LoginForm;
