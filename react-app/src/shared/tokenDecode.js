import jwt from "jsonwebtoken";

export const getPayload = (token) => {
  if (token) {
    return jwt.decode(token);
  }
  return {};
};

export const isExpired = (token) => {
  const payload = getPayload(token);
  const expirationDate = new Date(payload.exp * 1000);
  return expirationDate <= new Date();
};

export const getIdentity = (token) => {
  const payload = getPayload(token);
  if (payload.identity) {
    return payload.identity;
  }
  return null;
};
