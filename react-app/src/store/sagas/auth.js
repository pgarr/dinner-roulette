import { delay, put, call } from "redux-saga/effects";

import axios from "../../shared/axios-api";
import * as actions from "../actions/index";
import getPayload from "../../shared/tokenDecode";

export function* logoutSaga(action) {
  yield call([localStorage, "removeItem"], "access_token");
  yield call([localStorage, "removeItem"], "refresh_token");
  yield put(actions.logoutSucceed());
}

export function* checkAuthTimeoutSaga(action) {
  yield delay(action.expirationTime);
  if (action.refresh_token) {
    yield put(actions.refresh(action.refresh_token));
  } else {
    yield put(actions.logout());
  }
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
    yield put(
      actions.authSuccess(
        response.data.access_token,
        response.data.refresh_token
      )
    );
    const payload = getPayload(response.data.access_token);
    const expirationTime = yield payload.exp * 1000 - new Date().getTime();
    yield put(
      actions.checkAuthTimeout(expirationTime, response.data.refresh_token)
    );
  } catch (error) {
    yield put(actions.authFail(error));
  }
}

export function* authCheckStateSaga(action) {
  const access_token = yield localStorage.getItem("access_token");
  const refresh_token = yield localStorage.getItem("refresh_token");

  if (!access_token) {
    yield put(actions.logout());
  } else {
    const payload = getPayload(access_token);
    const expirationDate = yield new Date(payload.exp * 1000);
    if (expirationDate <= new Date()) {
      if (refresh_token) {
        yield put(actions.refresh(refresh_token));
      } else {
        yield put(actions.logout());
      }
    } else {
      yield put(actions.authSuccess(access_token, refresh_token));
      yield put(
        actions.checkAuthTimeout(
          expirationDate.getTime() - new Date().getTime(),
          refresh_token
        )
      );
    }
  }
}

export function* refreshAuthSaga(action) {
  try {
    const response = yield axios.post(
      "/auth/refresh",
      {},
      {
        headers: {
          Authorization: `Bearer ${action.refresh_token}`,
        },
      }
    );
    yield localStorage.setItem("access_token", response.data.access_token);
    yield put(
      actions.authSuccess(response.data.access_token, action.refresh_token)
    );
  } catch (error) {
    yield put(actions.logout());
  }
}
