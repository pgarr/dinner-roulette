import axios from "axios";

const instance = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

export const isErrorStatus = (error, status) => {
  return error.response && error.response.status === status;
};

export default instance;
