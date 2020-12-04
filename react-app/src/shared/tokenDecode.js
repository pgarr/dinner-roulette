import jwt from "jsonwebtoken";

const getPayload = (token) => {
  return jwt.decode(token);
};

export const isExpired = (token) => {
  const payload = getPayload(token);
  const expirationDate = new Date(payload.exp * 1000);
  return expirationDate <= new Date();
};

export default getPayload;
