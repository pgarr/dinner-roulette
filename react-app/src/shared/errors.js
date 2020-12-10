import { toast } from "react-toastify";

export const httpError = (code, log) => {
  toast.error(`Wystąpił błąd serwera (${code})`);
  console.log(log);
};
