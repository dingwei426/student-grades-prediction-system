import React from "react";
import { Link, useLocation } from "react-router-dom";
import utarLogo from "../assets/img/utar-logo.jpg";
import gearIcon from "../assets/img/gear-logo.png";
import "../assets/styles.css";

function SideNavBar() {
  const location = useLocation();
  const activePath = location.pathname;

  const navItems = [
    { path: "/home", label: "Grades and CGPA Prediction" },
    { path: "/history", label: "Prediction History" },
    { path: "/dashboard", label: "Prediction Dashboard" },
  ];

  const navItemStyle = (path) => ({
    textDecoration: "none",
    color: activePath === path ? "#03254c" : "#1167b1",
    fontSize: "16px",
    backgroundColor: activePath === path ? "#d0e6f8" : "transparent",
    fontWeight: activePath === path ? "600" : "500",
    padding: "10px",
    borderRadius: "4px",
    display: "block",
  });

  return (
    <nav className="side-nav">
      <div className="profile-section">
        <Link to="/home">
          <img src={utarLogo} alt="Profile" className="utar-img" />
        </Link>
        {/* <h2 className="welcome-text">Welcome, User</h2> */}
      </div>
      <hr className="separator" />

      <div className="nav-container">
        <ul className="nav-links">
          {navItems.map(({ path, label }) => (
            <li key={path}>
              <Link to={path} style={navItemStyle(path)}>
                {label}
              </Link>
            </li>
          ))}
        </ul>
      </div>

      <div className="bottom-section">
        <hr className="separator" />
        <div className="settings">
          <Link
            to="/settings"
            style={{
              textDecoration: "none",
              color: "#333",
              fontSize: "18px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor:
                activePath === "/setting" ? "#d0e6f8" : "transparent",
              padding: "10px",
              borderRadius: "4px",
            }}
          >
            <img src={gearIcon} alt="Settings" className="settings-icon" />
            Settings
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default SideNavBar;
