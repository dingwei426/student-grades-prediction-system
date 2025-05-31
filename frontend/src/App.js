import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Signup from "./pages/Signup.jsx";
import Login from "./pages/Login.jsx";
import Home from "./pages/Home.jsx";
import RecoverPassword from "./pages/RecoverPassword.jsx";
import ResetPassword from "./pages/ResetPassword.jsx";
import VerifyEmail from "./pages/VerifyEmail.jsx";
import PredictionHistory from "./pages/PredictionHistory.jsx";
import PredictionDetails from "./pages/PredictionDetails.jsx";
import PredictionDashboard from "./pages/PredictionDashboard.jsx";
import StudentSettings from "./pages/StudentSettings.jsx";

const App = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/recover-password" element={<RecoverPassword />} />
          <Route
            path="/reset-password/:reset_token"
            element={<ResetPassword />}
          />
          <Route path="/verify-email/:token" element={<VerifyEmail />} />
          <Route path="/history" element={<PredictionHistory />} />
          <Route path="/dashboard" element={<PredictionDashboard />} />
          <Route path="/prediction-details" element={<PredictionDetails />} />
          <Route path="/settings" element={<StudentSettings />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
