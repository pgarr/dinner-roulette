import * as actionTypes from "./actionTypes";

export const fetchRecipesSuccess = (recipes, activePage, totalPages) => {
  return {
    type: actionTypes.FETCH_RECIPES_SUCCESS,
    recipes: recipes,
    activePage: activePage,
    totalPages: totalPages,
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

export const fetchRecipes = (page) => {
  return {
    type: actionTypes.FETCH_RECIPES,
    page: page,
  };
};

export const changePage = (activePage) => {
  return {
    type: actionTypes.CHANGE_PAGE,
    activePage: activePage,
  };
};
