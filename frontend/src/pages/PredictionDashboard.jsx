import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import SideNavBar from "../components/SideNavBar";
import PageHeader from "../components/PageHeader";
import StatCard from "../components/StatCard";
import {
  Box,
  Card,
  CardContent,
  Typography,
  MenuItem,
  Select,
} from "@mui/material";
import { Bar, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  Tooltip,
  Legend,
  Title,
} from "chart.js";
import {
  fetchMostUsedModels,
  fetchPrimaryLanguageDistribution,
  fetchAverageRevisionTime,
  fetchCGPAComparison,
  fetchSubjectGradeDistribution,
  fetchQualificationTypeDistribution,
} from "../services/dashboardServices";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  Tooltip,
  Legend,
  Title
);

const PredictionDashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [modelStats, setModelStats] = useState({});
  const [languageStats, setLanguageStats] = useState({});
  const [revisionTime, setRevisionTime] = useState(0);
  const [qualificationType, setQualificationType] = useState({});
  const [cgpaData, setCgpaData] = useState({ labels: [], datasets: [] });
  const [gradeData, setGradeData] = useState({ labels: [], datasets: [] });
  const [subjects, setSubjects] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState(
    "PROGRAMMING AND PROBLEM SOLVING"
  );
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
      navigate("/login");
      return;
    }

    checkExpired();

    const loadData = async () => {
      try {
        const [
          models,
          langs,
          revision,
          cgpa,
          defaultSubjectData,
          qualification,
        ] = await Promise.all([
          fetchMostUsedModels(token),
          fetchPrimaryLanguageDistribution(token),
          fetchAverageRevisionTime(token),
          fetchCGPAComparison(token),
          fetchSubjectGradeDistribution(
            token,
            "PROGRAMMING AND PROBLEM SOLVING"
          ),
          fetchQualificationTypeDistribution(token),
        ]);

        setModelStats(models);
        setLanguageStats(langs);
        setRevisionTime(revision.average_revision_time);
        setQualificationType(qualification);

        // Sort CGPA data by actual_cgpa ascending
        const sortedCgpa = [...cgpa].sort((a, b) => {
          if (a.actual_cgpa === b.actual_cgpa) {
            return a.predicted_cgpa - b.predicted_cgpa;
          }
          return a.actual_cgpa - b.actual_cgpa;
        });
        const cgpaLabels = sortedCgpa.map(() => ""); // hides x-axis labels
        const predictedCgpaData = sortedCgpa.map((item) => item.predicted_cgpa);
        const actualCgpaData = sortedCgpa.map((item) => item.actual_cgpa);

        setCgpaData({
          labels: cgpaLabels,
          datasets: [
            {
              label: "Predicted CGPA",
              data: predictedCgpaData,
              borderColor: "#4dabf7",
              backgroundColor: "#4dabf7",
              tension: 0.3,
            },
            {
              label: "Input CGPA",
              data: actualCgpaData,
              borderColor: "#74c69d",
              backgroundColor: "#74c69d",
              tension: 0.3,
            },
          ],
        });

        // Define grade order
        const gradeOrder = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "F"];

        // Sort the defaultSubjectData based on the grade order
        const sortedDefaultSubjectData = gradeOrder
          .map((grade) =>
            defaultSubjectData.find((item) => item.grade === grade)
          )
          .filter(Boolean); // remove any undefined values

        setGradeData({
          labels: sortedDefaultSubjectData.map((item) => item.grade),
          datasets: [
            {
              data: sortedDefaultSubjectData.map((item) => item.count),
              backgroundColor: [
                "#DDE4ED",
                "#CCDBE9",
                "#B4C9DD",
                "#EDE1DB",
                "#F8EDEB",
                "#D8E2DC",
                "#ECE4DB",
                "#DEE2FF",
                "#CDEAC0",
              ],
            },
          ],
        });

        setSubjects([
          "ADVANCED DATABASE SYSTEMS",
          "ADVANCED WEB APPLICATION DEVELOPMENT",
          "ARTIFICIAL INTELLIGENCE",
          "CLOUD COMPUTING",
          "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY",
          "DATA MINING",
          "DATABASE SYSTEM FUNDAMENTALS",
          "DIGITAL IMAGE PROCESSING",
          "FUNDAMENTALS OF CYBERSECURITY",
          "HUMAN COMPUTER INTERACTION DESIGN",
          "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE",
          "MULTIMEDIA TECHNOLOGY",
          "NETWORK SECURITY MANAGEMENT",
          "OBJECT-ORIENTED APPLICATION DEVELOPMENT",
          "OPERATING SYSTEMS",
          "PARALLEL PROCESSING",
          "PROBABILITY AND STATISTICS FOR COMPUTING",
          "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS",
          "PROGRAMMING AND PROBLEM SOLVING",
          "PROGRAMMING WITH GAME ENGINES",
          "PROJECT",
          "SOFTWARE AND REQUIREMENTS",
          "SOFTWARE CONFIGURATION MANAGEMENT",
          "SOFTWARE CONSTRUCTION AND CONFIGURATION",
          "SOFTWARE DESIGN",
          "SOFTWARE ENTREPRENEURSHIP",
          "SOFTWARE PROJECT MANAGEMENT",
          "SOFTWARE QUALITY ASSURANCE",
          "SOFTWARE TESTING",
          "TCP/IP NETWORK APPLICATION DEVELOPMENT",
          "TCP/IP NETWORK FUNDAMENTALS",
          "TCP/IP NETWORK ROUTING",
          "TEAM PROJECT",
          "WEB APPLICATION DEVELOPMENT",
          "WIRELESS APPLICATION DEVELOPMENT",
        ]);
        setSelectedSubject("PROGRAMMING AND PROBLEM SOLVING");
      } catch (error) {
        console.error("Error loading dashboard data:", error);
        localStorage.removeItem("access_token");
        navigate("/login");
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [navigate, checkExpired]);

  const handleSubjectsubtitle = async (event) => {
    checkExpired();

    const subject = event.target.value;
    setSelectedSubject(subject);
    const gradeData = await fetchSubjectGradeDistribution(token, subject);

    // Define your desired grade order
    const gradeOrder = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "F"];

    // Sort the data based on the gradeOrder
    const sortedGradeData = gradeOrder
      .map((grade) => gradeData.find((item) => item.grade === grade))
      .filter(Boolean); // remove any undefined values (in case some grades are missing)

    setGradeData({
      labels: sortedGradeData.map((item) => item.grade),
      datasets: [
        {
          label: "Proportion",
          data: sortedGradeData.map((item) => item.count),
          backgroundColor: [
            "#DDE4ED",
            "#CCDBE9",
            "#B4C9DD",
            "#EDE1DB",
            "#F8EDEB",
            "#D8E2DC",
            "#ECE4DB",
            "#DEE2FF",
            "#CDEAC0",
          ],
        },
      ],
    });
  };

  const noDataPlugin = {
    id: "noData",
    beforeDraw: (chart) => {
      const datasets = chart.data.datasets;
      const hasData = datasets && datasets.some((ds) => ds.data.length > 0);

      if (!hasData) {
        const { ctx, width, height } = chart;
        ctx.save();
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.font = "20px sans-serif";
        ctx.fillStyle = "#666";
        ctx.fillText("No data available", width / 2, height / 2);
        ctx.restore();
      }
    },
  };

  return (
    <div>
      <SideNavBar />
      {loading && (
        <div className="loading-overlay">
          <div className="spinner" />
        </div>
      )}

      <div className="history-container">
        <div className="page-header-container">
          <PageHeader
            title="Prediction Dashboard"
            color="#1167b1"
            textAlign="center"
          />
        </div>

        {/* Display User Stats Cards */}
        <Box
          display="flex"
          gap={2}
          mb={4}
          sx={{ marginLeft: "auto", marginRight: "auto", width: "95%" }}
        >
          <StatCard
            title="Most Used Model"
            value={modelStats.model}
            subtitle={modelStats.percentage + " % of User Preference"}
            icon="🧠"
            backgroundColor="#DDE4ED"
          />
          <StatCard
            title="Most Common Primary Language"
            value={languageStats.language}
            subtitle={
              "Primary Language of " + languageStats.percentage + " % of User"
            }
            icon="🌐"
            backgroundColor="#CCDBE9"
            month={false}
          />
          <StatCard
            title="Most Common Qualification Type"
            value={qualificationType.qualification}
            subtitle={
              qualificationType.percentage +
              " % of User has " +
              qualificationType.qualification +
              " Qualification"
            }
            icon="🎓"
            backgroundColor="#B4C9DD"
            month={false}
          />
          <StatCard
            title="Average Revision Time"
            value={revisionTime + " Hours"}
            subtitle={"Average Revision Time is " + revisionTime + " Hours"}
            icon="👥"
            backgroundColor="#EDE1DB"
          />
        </Box>

        <Box
          display="flex"
          gap={2}
          flexWrap="wrap"
          sx={{ marginLeft: "auto", marginRight: "auto", width: "95%" }}
        >
          <Card
            sx={{
              flex: 1,
              minWidth: 400,
              backgroundColor: "#F0EFF4",
              borderRadius: 4,
            }}
          >
            <CardContent>
              <Typography variant="h6">Predicted Grade Distribution</Typography>
              <Select
                value={selectedSubject}
                onChange={handleSubjectsubtitle}
                fullWidth
                sx={{ mb: 2 }}
              >
                {subjects.map((subject, idx) => (
                  <MenuItem key={idx} value={subject}>
                    {subject}
                  </MenuItem>
                ))}
              </Select>
              <Bar
                data={gradeData}
                options={{
                  responsive: true,
                  plugins: {
                    noData: true, // You must define this even though it does nothing, to keep the plugin active
                    legend: {
                      display: false,
                    },
                    tooltip: {
                      callbacks: {
                        label: function (context) {
                          return `${context.raw}`;
                        },
                      },
                    },
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                      title: {
                        display: true,
                        text: "Count",
                      },
                    },
                    x: {
                      title: {
                        display: true,
                        text: "Grade",
                      },
                    },
                  },
                }}
                plugins={[noDataPlugin]}
              />
            </CardContent>
          </Card>
          <Card
            sx={{
              flex: 1,
              minWidth: 400,
              backgroundColor: "#EDE1DB",
              borderRadius: 4,
            }}
          >
            <CardContent>
              <Typography variant="h6">Predicted vs Input CGPA</Typography>
              <Line
                data={cgpaData}
                options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      display: true,
                      position: "top",
                    },
                    tooltip: {
                      mode: "index",
                      intersect: false,
                    },
                  },
                  scales: {
                    x: {
                      display: false, // hides the x-axis labels and grid lines
                    },
                    y: {
                      beginAtZero: true,
                      title: {
                        display: true,
                        text: "CGPA",
                      },
                    },
                  },
                }}
              />
            </CardContent>
          </Card>
        </Box>
      </div>
    </div>
  );
};

export default PredictionDashboard;
