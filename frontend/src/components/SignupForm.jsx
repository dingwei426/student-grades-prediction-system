import React from "react";
import InputWithLabel from "./InputWithLabel";
import LongButton from "./LongButton";

const SignupForm = ({
  email,
  password,
  setEmail,
  setPassword,
  showPassword,
  setShowPassword,
  handleSignup,
  errorMessage,
  successMessage,
  loading,
}) => {
  return (
    <form onSubmit={handleSignup} className="login-box">
      <p className="login-header">Signup Form</p>

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
      </div>

      <LongButton
        text={loading ? "Signing Up..." : "Signup"}
        type="submit"
        disabled={loading || !email || !password}
      />

      <div className="small-text">
        <p>
          Already have an account? <a href="./login">Login</a>
        </p>
      </div>
      {successMessage && <p className="success-message">{successMessage}</p>}
    </form>
  );
};

export default SignupForm;
