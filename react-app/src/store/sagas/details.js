import { put } from "redux-saga/effects";

import axios from "../../shared/axios-recipes";
import * as actions from "../actions/index";

export function* loadDetailsSaga(action) {
  yield put(actions.loadDetailsStart());
  try {
    const response = yield axios.get("/recipe/" + action.id);
    const loadedDetails = response.data.recipe;

    yield put(actions.loadDetailsSuccess(loadedDetails));
  } catch (error) {
    yield put(actions.loadDetailsFail(error));
  }
}
