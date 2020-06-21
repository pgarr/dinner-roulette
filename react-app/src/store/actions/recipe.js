import * as actionTypes from "./actionTypes";

export const fetchRecipesSuccess = (recipes) => {
  return {
    type: actionTypes.FETCH_RECIPES_SUCCESS,
    recipes: recipes,
  };
};

export const fetchRecipesFail = (error) => {
  return {
    type: actionTypes.FETCH_RECIPES_FAIL,
    error: error,
  };
};

export const fetchRecipesStart = () => {
  return {
    type: actionTypes.FETCH_RECIPES_START,
  };
};

export const fetchRecipes = () => {
  return {
    type: actionTypes.FETCH_RECIPES,
  };
};
