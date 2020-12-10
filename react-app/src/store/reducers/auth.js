import { httpError } from "../../shared/errors";
import * as actionTypes from "../actions/actionTypes";

const initialState = {
  access_token: null,
  refresh_token: null,
  error: null,
  loading: false,
  authRedirectPath: "/",
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.AUTH_START:
      return { ...state, error: null, loading: true };
    case actionTypes.AUTH_SUCCESS:
      return {
        ...state,
        access_token: action.access_token,
        refresh_token: action.refresh_token,
        error: null,
        loading: false,
      };
    case actionTypes.AUTH_FAIL:
      const res = action.errorResponse;
      let error = null;
      if (res.status === 401) {
        error = "Niepoprawna nazwa użytkownika lub hasło";
      } else {
        httpError(res.status, res);
      }
      return { ...state, error, loading: false };
    case actionTypes.AUTH_LOGOUT:
      return { ...state, access_token: null, refresh_token: null };
    case actionTypes.SET_AUTH_REDIRECT_PATH:
      return { ...state, authRedirectPath: action.path };
    default:
      return state;
  }
};

export default reducer;
