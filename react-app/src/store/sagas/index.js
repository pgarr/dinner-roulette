import { takeEvery, all } from "redux-saga/effects";

import * as actionTypes from "../actions/actionTypes";
import { fetchRecipesSaga } from "./recipes";
import { loadDetailsSaga } from "./details";
import {
  logoutSaga,
  checkAuthTimeoutSaga,
  authUserSaga,
  authCheckStateSaga,
} from "./auth";

export function* watchRecipes() {
  yield takeEvery(actionTypes.FETCH_RECIPES, fetchRecipesSaga);
}

export function* watchDetails() {
  yield takeEvery(actionTypes.LOAD_DETAILS, loadDetailsSaga);
}

export function* watchAuth() {
  yield all([
    takeEvery(actionTypes.AUTH_INITIATE_LOGOUT, logoutSaga),
    takeEvery(actionTypes.AUTH_CHECK_TIMEOUT, checkAuthTimeoutSaga),
    takeEvery(actionTypes.AUTH_USER, authUserSaga),
    takeEvery(actionTypes.AUTH_CHECK_STATE, authCheckStateSaga),
  ]);
}
