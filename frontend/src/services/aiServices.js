import axios from "./axiosInstance";

export const getAIRecommendation = async (token, predictionId) => {
  const response = await axios.get("/ai/retrieve_suggestion", {
    params: { prediction_id: predictionId },
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data.response;
};

export const generateAIRecommendation = async (token, predictionId) => {
  const response = await axios.get("/ai/openrouter_recommendation", {
    params: { prediction_id: predictionId },
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data.response;
};
