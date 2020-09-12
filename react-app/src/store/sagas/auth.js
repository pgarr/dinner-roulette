import { delay, put, call } from "redux-saga/effects";

import axios from "../../shared/axios-recipes";
import * as actions from "../actions/index";

export function* logoutSaga(action) {
  yield call([localStorage, "removeItem"], "access_token");
  yield call([localStorage, "removeItem"], "refresh_token");
  yield put(actions.logoutSucceed());
}

export function* checkAuthTimeoutSaga(action) {
  yield delay(action.expirationTime * 1000);
  yield put(actions.logout());
}

export function* authUserSaga(action) {
  yield put(actions.authStart());
  const authData = {
    username: action.username,
    password: action.password,
  };

  try {
    const response = yield axios.post("/auth/login", authData);

    yield localStorage.setItem("access_token", response.data.access_token);
    yield localStorage.setItem("refresh_token", response.data.refresh_token);

    yield put(actions.authSuccess(response.data.access_token, action.username)); // TODO: z tokena username
    // yield put(actions.checkAuthTimeout(response.data.expiresIn)); // TODO: z tokena expiresIn
  } catch (error) {
    yield put(actions.authFail(error.response.data));
  }
}

export function* authCheckStateSaga(action) {
  const token = yield localStorage.getItem("access_token");

  if (!token) {
    yield put(actions.logout());
  } else {
    // const expirationDate = yield new Date(
    //   localStorage.getItem("expirationDate")
    // );
    // if (expirationDate <= new Date()) {
    //   yield put(actions.logout());
    // } else {
    const username = "test"; // TODO: z tokena username
    yield put(actions.authSuccess(token, username));
    // yield put(
    //   actions.checkAuthTimeout(
    //     (expirationDate.getTime() - new Date().getTime()) / 1000
    //   )
    // );
    // }
  }
}
