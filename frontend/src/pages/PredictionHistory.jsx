import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import {
  getPredictionHistory,
  deletePrediction,
  editPredictionName,
} from "../services/predictionServices";
import SideNavBar from "../components/SideNavBar";
import PageHeader from "../components/PageHeader";
import ActionButtons from "../components/ActionButtons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faSort,
  faSortUp,
  faSortDown,
} from "@fortawesome/free-solid-svg-icons";
import "../assets/styles.css";

function PredictionHistory() {
  const navigate = useNavigate();
  const [historyItems, setHistoryItems] = useState([]);
  const [editId, setEditId] = useState(null);
  const [newName, setNewName] = useState("");
  const [loading, setLoading] = useState(true);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });
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
      setLoading(true);
      try {
        const response = await getPredictionHistory(token);
        if (response.predictions) {
          const formatted = response.predictions.map((item) => ({
            id: item.prediction_id,
            name: item.name,
            date: item.date.split(" ")[0],
            model: item.model_used,
            predicted_cgpa: item.predicted_cgpa,
          }));
          setHistoryItems(formatted);
        }
      } catch (err) {
        console.error("Error loading prediction history:", err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [navigate, checkExpired]);

  const handleSort = (key) => {
    checkExpired();
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }
    setSortConfig({ key, direction });
  };

  const sortedItems = [...historyItems].sort((a, b) => {
    if (!sortConfig.key) return 0;
    const aValue = a[sortConfig.key];
    const bValue = b[sortConfig.key];

    if (sortConfig.key === "date") {
      return sortConfig.direction === "asc"
        ? new Date(aValue) - new Date(bValue)
        : new Date(bValue) - new Date(aValue);
    }

    if (sortConfig.key === "predicted_cgpa") {
      return sortConfig.direction === "asc"
        ? parseFloat(aValue) - parseFloat(bValue)
        : parseFloat(bValue) - parseFloat(aValue);
    }

    return 0;
  });

  const handleDelete = async (id) => {
    checkExpired();
    try {
      await deletePrediction(token, id);
      setHistoryItems((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      console.error("Error deleting prediction:", err);
    }
  };

  const handleView = (id) => {
    checkExpired();
    navigate("/prediction-details", { state: { prediction_id: id } });
  };

  const handleEditClick = (id, currentName) => {
    checkExpired();
    setEditId(id);
    setNewName(currentName);
  };

  const handleSaveEdit = async (id) => {
    checkExpired();
    try {
      await editPredictionName(token, id, newName);
      setHistoryItems((prev) =>
        prev.map((item) => (item.id === id ? { ...item, name: newName } : item))
      );
      setEditId(null);
    } catch (err) {
      console.error("Update failed", err);
    }
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
            title="Prediction History"
            color="#1167b1"
            textAlign="center"
          />
        </div>
        <div className="table-wrapper">
          <table className="history-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Model</th>
                <th
                  onClick={() => handleSort("predicted_cgpa")}
                  style={{ cursor: "pointer" }}
                >
                  CGPA{" "}
                  <FontAwesomeIcon
                    icon={
                      sortConfig.key === "predicted_cgpa"
                        ? sortConfig.direction === "asc"
                          ? faSortUp
                          : faSortDown
                        : faSort
                    }
                  />
                </th>
                <th
                  onClick={() => handleSort("date")}
                  style={{ cursor: "pointer" }}
                >
                  Date{" "}
                  <FontAwesomeIcon
                    icon={
                      sortConfig.key === "date"
                        ? sortConfig.direction === "asc"
                          ? faSortUp
                          : faSortDown
                        : faSort
                    }
                  />
                </th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {sortedItems.length > 0 ? (
                sortedItems.map((item) => (
                  <tr key={item.id}>
                    <td>
                      {editId === item.id ? (
                        <input
                          type="text"
                          value={newName}
                          onChange={(e) => setNewName(e.target.value)}
                          className="edit-input"
                        />
                      ) : (
                        item.name
                      )}
                    </td>
                    <td>{item.model}</td>
                    <td>{item.predicted_cgpa}</td>
                    <td>{item.date}</td>
                    <td>
                      {editId === item.id ? (
                        <>
                          <button
                            className="save-button"
                            onClick={() => handleSaveEdit(item.id)}
                          >
                            Save
                          </button>
                          <button
                            className="cancel-button"
                            onClick={() => setEditId(null)}
                          >
                            Cancel
                          </button>
                        </>
                      ) : (
                        <>
                          <ActionButtons
                            onView={() => handleView(item.id)}
                            onDelete={() => handleDelete(item.id)}
                          />
                          <button
                            className="edit-button"
                            onClick={() => handleEditClick(item.id, item.name)}
                          >
                            Edit
                          </button>
                        </>
                      )}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="no-history">
                    No history available
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default PredictionHistory;
