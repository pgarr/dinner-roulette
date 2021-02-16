import reducer from "./auth";
import * as actionTypes from "../actions/actionTypes";

describe("auth reducer", () => {
  it("should return the initial state", () => {
    expect(reducer(undefined, {})).toEqual({
      access_token: null,
      refresh_token: null,
      error: null,
      loading: false,
      authRedirectPath: "/",
    });
  });

  it("should store the token upon login", () => {
    expect(
      reducer(
        {
          access_token: null,
          refresh_token: null,
          error: null,
          loading: false,
          authRedirectPath: "/",
        },
        {
          type: actionTypes.AUTH_SUCCESS,
          access_token: "some-access-token",
          refresh_token: "some-refresh-token",
        }
      )
    ).toEqual({
      access_token: "some-access-token",
      refresh_token: "some-refresh-token",
      error: null,
      loading: false,
      authRedirectPath: "/",
    });
  });
});
