import * as actionTypes from "../actions/actionTypes";

const initialState = {
  q: "",
  func: (q) => {},
  badges: [],
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.SET_SEARCH_Q:
      return { ...state, q: action.q };
    case actionTypes.SET_SEARCH_FUNCTION:
      return { ...state, func: action.func };
    case actionTypes.SET_SEARCH_BADGES:
      const badges = state.q.split(" ");
      return { ...state, badges: badges };
    default:
      return state;
  }
};

export default reducer;
