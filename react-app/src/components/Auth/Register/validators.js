import axios from "../../../shared/axios-recipes";

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
  let params = [];
  if (username !== null) {
    params.push("username=" + username);
  }
  if (email !== null) {
    params.push("email=" + email);
  }

  try {
    const response = await axios.get("/auth/validate?" + params.join("&"));

    let validationObject = {};
    for (const key in response.data) {
      switch (key) {
        case "username":
          validationObject = {
            ...validationObject,
            username: buildValidationProp(response.data[key], usernameMessages),
          };
          break;
        case "email":
          validationObject = {
            ...validationObject,
            email: buildValidationProp(response.data[key], emailMessages),
          };
          break;
        default:
          console.warn("Unknown validated property: " + key);
          break;
      }
    }
    return validationObject;
  } catch (error) {
    console.log(error); // TODO
  }
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

export const validateEmail = (email) => {};

export const validatePasswords = (password, password2) => {};
