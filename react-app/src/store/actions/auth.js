import * as actionTypes from "./actionTypes";

export const authStart = () => {
  return {
    type: actionTypes.AUTH_START,
  };
};

export const authSuccess = (access_token, refresh_token) => {
  return {
    type: actionTypes.AUTH_SUCCESS,
    access_token,
    refresh_token,
  };
};

export const authFail = (errorResponse) => {
  return {
    type: actionTypes.AUTH_FAIL,
    errorResponse,
  };
};

export const logout = () => {
  return {
    type: actionTypes.AUTH_INITIATE_LOGOUT,
  };
};

export const logoutSucceed = () => {
  return {
    type: actionTypes.AUTH_LOGOUT,
  };
};

export const checkAuthTimeout = (expirationTime, refresh_token) => {
  return {
    type: actionTypes.AUTH_CHECK_TIMEOUT,
    expirationTime,
    refresh_token,
  };
};

export const auth = (username, password) => {
  return {
    type: actionTypes.AUTH_USER,
    username,
    password,
  };
};

export const setAuthRedirectPath = (path) => {
  return {
    type: actionTypes.SET_AUTH_REDIRECT_PATH,
    path,
  };
};

export const authCheckState = () => {
  return {
    type: actionTypes.AUTH_CHECK_STATE,
  };
};

export const refresh = (refresh_token) => {
  return {
    type: actionTypes.AUTH_INITIATE_REFRESH,
    refresh_token,
  };
};
