import React, { useReducer } from "react";
import { Redirect } from "react-router-dom";
import { Form, Button } from "react-bootstrap";

import {
  validatePassword,
  validatePassword2,
  buildValidationObject,
} from "../Register/validators";
import { isExpired } from "../../../shared/tokenDecode";
import axios, { isErrorStatus } from "../../../shared/axios-api";
import { inputChangedDispatch } from "../../../shared/handlers";
import useDebouncedEffect from "../../../shared/customHooks/useDebouncedEffect";
import ModalWithBackdrop from "../../UI/ModalWithBackdrop/ModalWithBackdrop";
import InlineFormField from "../../UI/InlineFormField/InlineFormField";
import { axiosError } from "../../../shared/errors";
import AuthForbidden from "../../HOC/AuthForbidden";
import useValueValidation from "../../../shared/customHooks/useValueValidation";

const setPasswordReducer = (state, action) => {
  switch (action.type) {
    case "INIT_REQUEST":
      return {
        ...state,
        validated: false,
        changed: false,
        confirmed: false,
        error401: false,
        loading: true,
      };
    case "REQUEST_SUCCESS":
      return { ...state, validated: true, changed: true, loading: false };
    case "REQUEST_FAIL":
      return { ...state, loading: false };
    case "ERROR_401":
      return { ...state, error401: true };
    case "MODAL_CONFIRMED":
      return { ...state, confirmed: true };
    default:
      return { ...state };
  }
};

const SetPassword = ({ match }) => {
  const [
    { validated, changed, confirmed, error401, loading },
    dispatch,
  ] = useReducer(setPasswordReducer, {
    validated: false,
    changed: false,
    confirmed: false,
    error401: false,
    loading: false,
  });

  const [password, dispatchPassword] = useValueValidation("");
  const [password2, dispatchPassword2] = useValueValidation("");

  const validationDelay = 1000;

  // validate password
  useDebouncedEffect(
    () => {
      if (password.touched) {
        const result = validatePassword(password.value);
        dispatchPassword({ type: "SET_VALIDATION", ...result });
      }
    },
    validationDelay,
    [password.value]
  );

  // validate password2
  useDebouncedEffect(
    () => {
      if (password2.touched) {
        const result = validatePassword2(password.value, password2.value);
        dispatchPassword2({ type: "SET_VALIDATION", ...result });
      }
    },
    validationDelay,
    [password.value, password2.value]
  );

  const submitHandler = async (event) => {
    event.preventDefault();
    dispatch({ type: "INIT_REQUEST" });
    try {
      await axios.post("/auth/reset_password/" + match.params.token, {
        password: password.value,
      });
      dispatch({ type: "REQUEST_SUCCESS" });
    } catch (error) {
      if (isErrorStatus(error, 422)) {
        const result = buildValidationObject(error.response.data);
        dispatchPassword({ type: "SET_VALIDATION", ...result.password });
      } else if (isErrorStatus(error, 401)) {
        dispatch({ type: "ERROR_401" });
      } else {
        axiosError(error);
        dispatch({ type: "REQUEST_FAIL" });
      }
    }
  };

  let redirect = null;
  if (confirmed) {
    redirect = <Redirect to={"/login"} />;
  }

  return (
    <AuthForbidden>
      {redirect}

      <ModalWithBackdrop
        show={changed && !confirmed}
        onHide={() => {
          dispatch({ type: "MODAL_CONFIRMED" });
        }}
        title="Sukces!"
        text="Hasło zostało zmienione. Zaloguj się za pomocą podanych danych."
      />

      <h1>Resetowanie hasła</h1>
      {isExpired(match.params.token) || error401 ? (
        <React.Fragment>
          <p>Link resetowania hasła wygasł.</p>
          <Button href="/resetrequest" variant="outline-info">
            Wyślij ponownie
          </Button>
        </React.Fragment>
      ) : (
        <Form noValidate validated={validated} onSubmit={submitHandler}>
          <InlineFormField
            controlId="formPassword"
            labelText="Hasło"
            type="password"
            errors={password.errors}
            value={password.value}
            onChangeHandler={(event) => {
              inputChangedDispatch(event, dispatchPassword);
            }}
            isValid={password.touched && password.valid}
            isInvalid={password.touched && !password.valid}
            disabled={loading}
          />
          <InlineFormField
            controlId="formPassword2"
            labelText="Powtórz hasło"
            type="password"
            errors={password2.errors}
            value={password2.value}
            onChangeHandler={(event) => {
              inputChangedDispatch(event, dispatchPassword2);
            }}
            isValid={password2.touched && password2.valid}
            isInvalid={password2.touched && !password2.valid}
            disabled={loading}
          />
          <Button
            variant="secondary"
            type="submit"
            disabled={!password.valid || !password2.valid || loading}
          >
            Zmień hasło
          </Button>
        </Form>
      )}
    </AuthForbidden>
  );
};

export default SetPassword;
