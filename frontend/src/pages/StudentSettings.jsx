import React, { useState, useEffect, useCallback } from "react";
import {
  getDefaultStudentFields,
  updateDefaultStudentFields,
} from "../services/predictionServices";
import { jwtDecode } from "jwt-decode";
import { changePassword } from "../services/authServices";
import SideNavBar from "../components/SideNavBar";
import PageHeader from "../components/PageHeader";
import { InputWithLabel, SelectWithLabel } from "../components/SelectWithLabel";
import { useNavigate } from "react-router-dom";
import LongButton from "../components/LongButton";
import LogoutIcon from "../assets/img/logout.png";
import { AiOutlineLoading3Quarters } from "react-icons/ai";

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    marginLeft: "22%",
    backgroundColor: "#fff",
    minHeight: "90vh",
    padding: "20px",
    position: "relative",
  },
  section: {
    backgroundColor: "#f5f5f5",
    borderRadius: "10px",
    padding: "20px",
    marginBottom: "20px",
    boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
  },
  sectionHeader: {
    fontSize: "18px",
    fontWeight: "bold",
    marginBottom: "20px",
    color: "#1167b1",
  },
  logoutIconContainer: {
    display: "flex",
    alignItems: "center",
    cursor: "pointer",
    padding: "10px",
    transition: "background-color 0.2s ease",
  },
  logoutIcon: {
    width: "30px",
    height: "30px",
    transition: "transform 0.2s ease",
  },
  logoutText: {
    marginRight: "20px",
    fontSize: "16px",
    color: "#2f527a",
    fontWeight: "600",
    opacity: 0,
    transition: "opacity 0.2s ease",
  },
  logoutIconHover: {
    transform: "scale(1.1)",
    backgroundColor: "#e9e9e9",
    borderRadius: "5px",
    boxShadow: "0 0 20px rgba(0, 0, 0, 0.2)",
  },
  logoutTextVisible: {
    opacity: 1,
  },
  spinnerIcon: {
    marginRight: "0.5em",
    animation: "spin 1s linear infinite",
  },
  // Confirmation modal styles
  confirmOverlay: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "rgba(0,0,0,0.4)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 2000,
  },
  confirmContent: {
    backgroundColor: "#fff",
    padding: "24px 32px",
    borderRadius: 8,
    boxShadow: "0 2px 10px rgba(0,0,0,0.2)",
    textAlign: "center",
    minWidth: 300,
  },
  confirmButton: {
    marginTop: 16,
    padding: "8px 16px",
    border: "none",
    borderRadius: 4,
    backgroundColor: "#1976d2",
    color: "#fff",
    cursor: "pointer",
  },
};

function StudentSettings() {
  const navigate = useNavigate();
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [logoutHover, setLogoutHover] = useState(false);

  const [gender, setGender] = useState("Female");
  const [yob, setYob] = useState("");
  const [primaryLanguage, setPrimaryLanguage] = useState("English");
  const [englishProficiency, setEnglishProficiency] = useState();
  const [yearTrimester, setYearTrimester] = useState("Year 1 Trimester 1");

  const [schoolLocation, setSchoolLocation] = useState("Johor");
  const [scienceStream, setScienceStream] = useState("No");
  const [qualification, setQualification] = useState("UEC");
  const [grades, setGrades] = useState("Mostly A's");
  const [assignmentFrequency, setAssignmentFrequency] = useState("Never");
  const [computerInterest, setComputerInterest] = useState();
  const [studyHours, setStudyHours] = useState();
  const [cgpa, setCgpa] = useState();
  const [confirmMessage, setConfirmMessage] = useState("");
  const [changingPassword, setChangingPassword] = useState(false);
  const [saveDefaultsLoading, setSaveDefaultsLoading] = useState(false);

  const token = localStorage.getItem("access_token");
  const checkExpired = useCallback(() => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    try {
      const decoded = jwtDecode(token);
      const currentTime = Date.now() / 1000;

      if (decoded.exp < currentTime) {
        window.alert("Your session has expired. Please log in again.");
        localStorage.removeItem("access_token");
        navigate("/login");
      }
    } catch (err) {
      console.error("Token decoding failed:", err);
      window.alert("Invalid session detected. Please log in again.");
      localStorage.removeItem("access_token");
      navigate("/login");
    }
  }, [navigate]);

  useEffect(() => {
    if (!token) {
      navigate("/login"); // Redirect to login if no token
      return;
    }
    checkExpired();

    const fetchDefaults = async () => {
      try {
        const data = await getDefaultStudentFields(token);

        setGender(data.gender || "Female");
        setYob(data.yob || "2000");
        setPrimaryLanguage(data.primary_language || "English");
        setEnglishProficiency(data.english_proficiency || "1");
        setYearTrimester(data.year_trimester || "Year 1 Trimester 1");

        setSchoolLocation(data.secondary_school_location || "Johor");
        setScienceStream(
          data.science_stream ? (data.science_stream ? "Yes" : "No") : "No"
        );
        setQualification(data.qualification || "UEC");
        setGrades(data.qualification_grades || "Mostly A's");
        setAssignmentFrequency(data.assignment_working_frequency || "Never");
        setComputerInterest(data.computer_interest || "1");
        setStudyHours(data.average_studying_hour || "0");
        setCgpa(data.cgpa || "0.0000");
      } catch (error) {
        console.error("Failed to load default fields:", error);
      }
    };

    fetchDefaults();
  }, [token, navigate, checkExpired]);

  // Update default student fields using the axios instance via the API service
  const handleSaveDefaults = async () => {
    checkExpired();
    setSaveDefaultsLoading(true);

    const payload = {
      gender,
      yob: Number(yob),
      primary_language: primaryLanguage,
      english_proficiency: Number(englishProficiency),
      year_trimester: yearTrimester,
      secondary_school_location: schoolLocation,
      science_stream: scienceStream === "Yes", // convert to boolean
      qualification,
      qualification_grades: grades,
      assignment_working_frequency: assignmentFrequency,
      computer_interest: Number(computerInterest),
      average_studying_hour: Number(studyHours),
      cgpa: Number(cgpa),
    };

    try {
      console.log("Payload:", payload); // Log the payload to see what is being sent
      await updateDefaultStudentFields(token, payload);
      setConfirmMessage("Default student profile saved!");
    } catch (error) {
      console.error("Error updating profile defaults:", error);
    } finally {
      setSaveDefaultsLoading(false);
    }
  };

  const handleChangePassword = async () => {
    checkExpired();
    setError("");
    setSuccess("");

    if (newPassword !== confirmNewPassword) {
      setError("New passwords do not match");
      return;
    }
    setChangingPassword(true);

    try {
      await changePassword(
        currentPassword,
        newPassword,
        confirmNewPassword,
        token
      );

      setConfirmMessage("Password changed successfully!");
      setSuccess("Password changed successfully!");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmNewPassword("");
    } catch (err) {
      console.error("Error changing password:", err);
      // Display error message coming from the server, if available
      setError(
        err.response?.data?.error || "An error occurred. Please try again."
      );
    } finally {
      setChangingPassword(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  return (
    <div>
      <SideNavBar />
      <div style={styles.container}>
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "20px",
          }}
        >
          <PageHeader title="Settings" color="#1167b1" textAlign="left" />
          <div
            style={styles.logoutIconContainer}
            onClick={handleLogout}
            onMouseOver={() => setLogoutHover(true)}
            onMouseOut={() => setLogoutHover(false)}
          >
            <span
              style={{
                ...styles.logoutText,
                ...(logoutHover ? styles.logoutTextVisible : {}),
              }}
            >
              Logout
            </span>
            <img
              src={LogoutIcon}
              alt="Logout"
              style={{
                ...styles.logoutIcon,
                ...(logoutHover ? styles.logoutIconHover : {}),
              }}
            />
          </div>
        </div>

        {/* Account Security Section */}
        <div style={styles.section}>
          <h2 style={styles.sectionHeader}>Account Security</h2>
          <InputWithLabel
            label="Current Password"
            type="password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
          />
          <InputWithLabel
            label="New Password"
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <InputWithLabel
            label="Confirm New Password"
            type="password"
            value={confirmNewPassword}
            onChange={(e) => setConfirmNewPassword(e.target.value)}
          />
          {error && (
            <div style={{ color: "red", marginBottom: "10px" }}>{error}</div>
          )}
          {success && (
            <div style={{ color: "green", marginBottom: "10px" }}>
              {success}
            </div>
          )}
          <div style={{ width: "30%" }}>
            <LongButton
              text={
                changingPassword ? (
                  <>
                    <AiOutlineLoading3Quarters style={styles.spinnerIcon} />
                    Changing…
                  </>
                ) : (
                  "Confirm Password Change"
                )
              }
              onClick={handleChangePassword}
              disabled={changingPassword}
            />
          </div>
        </div>

        {/* Set Default Student Profile Section */}
        <div style={styles.section}>
          <h2 style={styles.sectionHeader}>Set Default Student Profile</h2>

          <SelectWithLabel
            label="Gender"
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            options={["Female", "Male"]}
          />

          <InputWithLabel
            label="Year of Birth"
            type="number"
            value={yob}
            onChange={(e) => setYob(e.target.value)}
          />

          <SelectWithLabel
            label="Primary Language"
            value={primaryLanguage}
            onChange={(e) => setPrimaryLanguage(e.target.value)}
            options={["English", "Chinese", "Malay", "Other"]}
          />

          <InputWithLabel
            label="English Proficiency (1 - 5)"
            type="number"
            value={englishProficiency}
            onChange={(e) => {
              let val = parseFloat(e.target.value);
              if (isNaN(val)) val = 0;
              if (val < 0) val = 0;
              if (val > 5) val = 5;
              setEnglishProficiency(val);
            }}
          />

          <SelectWithLabel
            label="Academic Year & Trimester"
            value={yearTrimester}
            onChange={(e) => setYearTrimester(e.target.value)}
            options={[
              "Year 1 Trimester 1",
              "Year 1 Trimester 2",
              "Year 1 Trimester 3",
              "Year 2 Trimester 1",
              "Year 2 Trimester 2",
              "Year 2 Trimester 3",
              "Year 3 Trimester 1",
              "Year 3 Trimester 2",
              "Year 3 Trimester 3",
              "Alumni",
            ]}
          />

          <SelectWithLabel
            label="Secondary School Location"
            value={schoolLocation}
            onChange={(e) => setSchoolLocation(e.target.value)}
            options={[
              "Johor",
              "Kedah",
              "Kelantan",
              "Kuala Lumpur",
              "Labuan",
              "Malacca",
              "Negeri Sembilan",
              "Pahang",
              "Penang",
              "Perak",
              "Perlis",
              "Putrajaya",
              "Sabah",
              "Sarawak",
              "Selangor",
              "Terengganu",
            ]}
          />

          <SelectWithLabel
            label="Science Stream in High School"
            value={scienceStream}
            onChange={(e) => setScienceStream(e.target.value)}
            options={["Yes", "No"]}
          />

          <SelectWithLabel
            label="Completed Qualification"
            value={qualification}
            onChange={(e) => setQualification(e.target.value)}
            options={[
              "UEC",
              "Foundation in Art",
              "Foundation in Science",
              "Diploma",
              "A-Level",
              "STPM",
            ]}
          />

          <SelectWithLabel
            label="Qualification Grades"
            value={grades}
            onChange={(e) => setGrades(e.target.value)}
            options={[
              "Mostly A's",
              "Mostly B's",
              "Mostly C's",
              "Mostly D's",
              "Mostly E/F's",
              "N/A",
            ]}
          />

          <SelectWithLabel
            label="Assignment Collaboration Frequency"
            value={assignmentFrequency}
            onChange={(e) => setAssignmentFrequency(e.target.value)}
            options={["Never", "Sometimes", "Often", "Very-often"]}
          />

          <InputWithLabel
            label="Computer Interest (1 - 5)"
            type="number"
            value={computerInterest}
            onChange={(e) => {
              let val = parseFloat(e.target.value);
              if (isNaN(val)) val = 0;
              if (val < 0) val = 0;
              if (val > 5) val = 5;
              setComputerInterest(val);
            }}
          />

          <InputWithLabel
            label="Weekly Study Hours (Excl. Classes)"
            type="number"
            value={studyHours}
            onChange={(e) => setStudyHours(e.target.value)}
          />

          <InputWithLabel
            label="Current CGPA"
            type="number"
            step={0.01}
            value={cgpa}
            onChange={(e) => {
              let val = parseFloat(e.target.value);
              if (isNaN(val)) val = 0;
              if (val < 0) val = 0;
              if (val > 4) val = 4;
              setCgpa(val);
            }}
          />

          <LongButton
            text={
              saveDefaultsLoading ? (
                <>
                  <AiOutlineLoading3Quarters style={styles.spinnerIcon} />
                  Saving…
                </>
              ) : (
                "Save Student Profile Defaults"
              )
            }
            onClick={handleSaveDefaults}
            disabled={saveDefaultsLoading}
          />
        </div>
      </div>
      {/* Confirmation Modal */}
      {confirmMessage && (
        <div style={styles.confirmOverlay}>
          <div style={styles.confirmContent}>
            <p>{confirmMessage}</p>
            <button
              style={styles.confirmButton}
              onClick={() => setConfirmMessage("")}
            >
              OK
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default StudentSettings;
