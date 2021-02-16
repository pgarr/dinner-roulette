import * as actionTypes from "./actionTypes";

export const setSearchQ = (q) => {
  return {
    type: actionTypes.SET_SEARCH_Q,
    q,
  };
};

export const setSearchFunction = (func) => {
  return {
    type: actionTypes.SET_SEARCH_FUNCTION,
    func,
  };
};

export const setSearchBadges = () => {
  return {
    type: actionTypes.SET_SEARCH_BADGES,
  };
};
