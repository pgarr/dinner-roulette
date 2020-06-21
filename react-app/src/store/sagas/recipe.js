import { put } from "redux-saga/effects";

import axios from "../../shared/axios-recipes";
import * as actions from "../actions/index";

export function* fetchRecipesSaga(action) {
  yield put(actions.fetchRecipesStart());
  try {
    const queryParams = "?page=" + action.page;
    const response = yield axios.get("/recipes" + queryParams);
    const fetchedRecipes = response.data.recipes;
    const totalPages = response.data._meta.total_pages;
    const activePage = response.data._meta.page;
    yield put(
      actions.fetchRecipesSuccess(fetchedRecipes, activePage, totalPages)
    );
  } catch (error) {
    yield put(actions.fetchRecipesFail(error));
  }
}
