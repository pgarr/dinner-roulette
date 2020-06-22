import * as actionTypes from "../actions/actionTypes";

const initalState = {
  loading: false,
  title: "",
  author: "",
  time: 0,
  difficulty: 0,
  ingredients: [],
  preparation: "",
  link: "",
};

const reducer = (state = initalState, action) => {
  switch (action.type) {
    case actionTypes.LOAD_DETAILS_START:
      return { ...state, loading: true };
    case actionTypes.LOAD_DETAILS_SUCCESS:
      return {
        ...state,
        title: action.details.title,
        author: action.details.author,
        time: action.details.time,
        difficulty: action.details.difficulty,
        ingredients: action.details.ingredients,
        preparation: action.details.preparation,
        link: action.details.link,
        loading: false,
      };
    case actionTypes.LOAD_DETAILS_FAIL:
      return { ...state, loading: false };
    default:
      return { ...state };
  }
};

export default reducer;
