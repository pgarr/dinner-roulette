import * as actionTypes from "../actions/actionTypes";

const initalState = {
  recipes: [],
  loading: false,
};

const reducer = (state = initalState, action) => {
  switch (action.type) {
    case actionTypes.FETCH_RECIPES_START:
      return { ...state, loading: true };
    case actionTypes.FETCH_RECIPES_SUCCESS:
      return { ...state, recipes: action.recipes, loading: false };
    case actionTypes.FETCH_RECIPES_FAIL:
      return { ...state, loading: false };
    default:
      return { ...state };
  }
};

export default reducer;
