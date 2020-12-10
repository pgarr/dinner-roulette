import axios from "../../../shared/axios-api";

import { httpError } from "../../../shared/errors";

const usernameMessages = {
  unique: "Nazwa jest już zajęta",
  min_length: "Nazwa zbyt krótka",
};

const emailMessages = {
  unique: "Ten adres jest już używany",
  format: "Niepoprawny adres email",
};

const passwordMessages = {
  min_length: "Hasło zbyt krótkie",
  equal: "Hasła różnią się od siebie",
};

export const validateOnBackend = async (username, email) => {
  let params = {};
  if (username !== null) {
    params = { ...params, username };
  }
  if (email !== null) {
    params = { ...params, email };
  }

  try {
    const response = await axios.post("/auth/validate", params);

    return buildValidationObject(response.data);
  } catch (error) {
    httpError(error.response.status, error.response);
  }
};

export const buildValidationObject = (data) => {
  let validationObject = {};
  for (const key in data) {
    switch (key) {
      case "username":
        validationObject = {
          ...validationObject,
          username: buildValidationProp(data[key], usernameMessages),
        };
        break;
      case "email":
        validationObject = {
          ...validationObject,
          email: buildValidationProp(data[key], emailMessages),
        };
        break;
      case "password":
        validationObject = {
          ...validationObject,
          password: buildValidationProp(data[key], passwordMessages),
        };
        break;
      default:
        console.warn("Unknown validated property: " + key);
        break;
    }
  }
  return validationObject;
};

const buildValidationProp = (validationResult, messages) => {
  const errors = [];

  for (const check in validationResult.checks) {
    if (!validationResult.checks[check]) {
      errors.push(messages[check]);
    }
  }

  return { valid: validationResult.valid, errors };
};

export const validatePassword = (password) => {
  const errors = [];

  const min_length = password.length > 5;
  if (!min_length) {
    errors.push(passwordMessages.min_length);
  }

  return { valid: min_length, errors };
};

export const validatePassword2 = (password, password2) => {
  const errors = [];

  const equal = password === password2;
  if (!equal) {
    errors.push(passwordMessages.equal);
  }

  return { valid: equal, errors };
};
