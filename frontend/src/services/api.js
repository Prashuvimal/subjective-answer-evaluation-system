import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

export const extractOCR = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return API.post("/ocr", formData);
};

export const evaluateAnswer = (payload) => {
  return API.post("/evaluate", payload);
};
