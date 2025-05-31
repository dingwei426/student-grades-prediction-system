import axios from "./axiosInstance";

export const login = async (email, password) => {
  return axios.post("/auth/login", { email, password });
};

export const admin = async (token) => {
  return axios.get("/admin/admin", {
    headers: {
      Authorization: `Bearer ${token}`, // Pass the token in the Authorization header
    },
  });
};

export const profile = async () => {
  return axios.get("/profile/profile");
};

export const signup = async (email, password) => {
  return axios.post("/auth/signup", { email, password });
};

export const recoverPassword = async (email) => {
  return axios.post("/auth/recover-password", { email });
};

export const resetPassword = async (reset_token, new_password) => {
  return axios.post("/auth/reset-password", { reset_token, new_password });
};

export const verifyEmail = async (token) => {
  return axios.get(`/auth/verify-email/${token}`);
};

export const changePassword = async (
  current_password,
  new_password,
  confirm_password,
  token
) => {
  const response = await axios.post(
    "http://localhost:5000/auth/change-password",
    {
      current_password: current_password,
      new_password: new_password,
      confirm_password: confirm_password,
    },
    {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    }
  );
  return response.data;
};
