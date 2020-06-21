import { takeEvery } from "redux-saga/effects";

import * as actionTypes from "../actions/actionTypes";
import { fetchRecipesSaga } from "./recipe";

export function* watchRecipe() {
  yield takeEvery(actionTypes.FETCH_RECIPES, fetchRecipesSaga);
}
