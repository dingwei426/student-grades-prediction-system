import axios from "./axiosInstance";

export const fetchMostUsedModels = async (token) => {
  try {
    const response = await axios.get("/dashboard/most_used_models", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching most used models:", error);
    throw error;
  }
};

export const fetchSubjectGradeDistribution = async (token, subject) => {
  try {
    const response = await axios.get("/dashboard/subject_grade_distribution", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params: {
        subject,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching subject grade distribution:", error);
    throw error;
  }
};

export const fetchPrimaryLanguageDistribution = async (token) => {
  try {
    const response = await axios.get(
      "/dashboard/primary_language_distribution",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching primary language distribution:", error);
    throw error;
  }
};

export const fetchAverageRevisionTime = async (token) => {
  try {
    const response = await axios.get("/dashboard/average_revision_time", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching average revision time:", error);
    throw error;
  }
};

export const fetchCGPAComparison = async (token) => {
  try {
    const response = await axios.get("/dashboard/cgpa_comparison", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching CGPA comparison:", error);
    throw error;
  }
};

export const fetchQualificationTypeDistribution = async (token) => {
  try {
    const response = await axios.get("/dashboard/qualification_distribution", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching qualification type distribution:", error);
    throw error;
  }
};
