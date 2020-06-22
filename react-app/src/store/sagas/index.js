import { takeEvery } from "redux-saga/effects";

import * as actionTypes from "../actions/actionTypes";
import { fetchRecipesSaga } from "./recipes";
import { loadDetailsSaga } from "./details";

export function* watchRecipes() {
  yield takeEvery(actionTypes.FETCH_RECIPES, fetchRecipesSaga);
}

export function* watchDetails() {
  yield takeEvery(actionTypes.LOAD_DETAILS, loadDetailsSaga);
}
