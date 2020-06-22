import * as actionTypes from "./actionTypes";

export const loadDetailsFail = (error) => {
  return {
    type: actionTypes.LOAD_DETAILS_FAIL,
    error: error,
  };
};

export const loadDetailsStart = () => {
  return {
    type: actionTypes.LOAD_DETAILS_START,
  };
};

export const loadDetailsSuccess = (details) => {
  return {
    type: actionTypes.LOAD_DETAILS_SUCCESS,
    details: details,
  };
};

export const loadDetails = (id) => {
  return {
    type: actionTypes.LOAD_DETAILS,
    id: id,
  };
};
