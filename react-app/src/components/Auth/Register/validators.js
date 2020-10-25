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

export const validateUsername = async (username) => {
  const queryParams = "?username=" + username;

  try {
    const response = await axios.get("/auth/validate" + queryParams);
    const result = response.data.username;

    let error = null;
    if (!result.valid) {
      if (!result.checks.unique) {
        error = usernameMessages.unique;
      } else if (!result.checks.min_length) {
        error = usernameMessages.min_length;
      }
    }
    return {
      valid: result.valid,
      error,
    };
  } catch (error) {
    console.log(error); // TODO
  }
};

export const validateEmail = (email) => {};

export const validatePasswords = (password, password2) => {};
