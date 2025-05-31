import axios from "./axiosInstance";

export const predict = async (token, requestData) => {
  try {
    const response = await axios.post("/prediction/predict", requestData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Prediction API call failed:", error);
    throw error;
  }
};

export const getPredictionHistory = async (token) => {
  try {
    const response = await axios.get(`/prediction/get_predictions`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching prediction history:", error);
    throw error;
  }
};

export const getPredictionDetails = async (token, predictionId) => {
  try {
    const response = await axios.get("/prediction/get_prediction", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params: {
        prediction_id: predictionId,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching prediction details:", error);
    throw error;
  }
};

export const deletePrediction = async (token, predictionId) => {
  try {
    const response = await axios.delete(
      `/prediction/delete_prediction/${predictionId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error deleting prediction:", error);
    throw error;
  }
};

export const editPredictionName = async (token, predictionId, newName) => {
  try {
    const response = await axios.put(
      `/prediction/update_prediction_name/${predictionId}`,
      { new_name: newName },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error updating prediction name:", error);
    throw error;
  }
};

export const getDefaultStudentFields = async (token) => {
  try {
    const response = await axios.get(`/prediction/get_default_field`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching default student fields:", error);
    throw error;
  }
};

export const updateDefaultStudentFields = async (token, payload) => {
  try {
    const response = await axios.post(
      "/prediction/update_default_field",
      payload,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error updating default student fields:", error);
    throw error;
  }
};
