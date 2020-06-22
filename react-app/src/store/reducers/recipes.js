import * as actionTypes from "../actions/actionTypes";

const initalState = {
  recipes: [],
  activePage: 1,
  totalPages: 1,
  loading: false,
};

const reducer = (state = initalState, action) => {
  switch (action.type) {
    case actionTypes.FETCH_RECIPES_START:
      return { ...state, loading: true };
    case actionTypes.FETCH_RECIPES_SUCCESS:
      return {
        ...state,
        recipes: action.recipes,
        totalPages: action.totalPages,
        activePage: action.activePage,
        loading: false,
      };
    case actionTypes.FETCH_RECIPES_FAIL:
      return { ...state, loading: false };
    case actionTypes.CHANGE_PAGE:
      return { ...state, activePage: parseInt(action.activePage) };
    default:
      return { ...state };
  }
};

export default reducer;
