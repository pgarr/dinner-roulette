import { toast } from "react-toastify";

export const axiosError = (error) => {
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of valid status codes
    toast.error(`Wystąpił błąd serwera (${error.response.status})`);
    console.log(error.response);
  } else if (error.request) {
    // The request was made but no response was received
    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
    // http.ClientRequest in node.js
    toast.error("Wystąpił błąd komunikacji");
    console.log(error.request);
  } else {
    // Something happened in setting up the request that triggered an Error
    toast.error("Wystąpił błąd");
    console.log(error.message);
  }
};
