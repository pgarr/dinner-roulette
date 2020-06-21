import { put } from "redux-saga/effects";

import axios from "../../shared/axios-recipes";
import * as actions from "../actions/index";

export function* fetchRecipesSaga(action) {
  yield put(actions.fetchRecipesStart());
  try {
    const response = yield axios.get("/recipes");
    const fetchedRecipes = response.data.recipes;
    yield put(actions.fetchRecipesSuccess(fetchedRecipes));
  } catch (error) {
    yield put(actions.fetchRecipesFail(error));
  }
}
