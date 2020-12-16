import React, { useState } from "react";
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

const SetPassword = ({ match }) => {
  const [validated, setValidated] = useState(false); // TODO useReducer
  const [changed, setChanged] = useState(false);
  const [confirmed, setConfirmed] = useState(false);
  const [error401, setError401] = useState(false);

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

    // TODO: loading state (disabled form)
    try {
      await axios.post("/auth/reset_password/" + match.params.token, {
        password: password.value,
      });
      setValidated(true);
      setChanged(true);
    } catch (error) {
      setValidated(false);
      if (isErrorStatus(error, 422)) {
        const result = buildValidationObject(error.response.data);
        dispatchPassword({ type: "SET_VALIDATION", ...result.password });
      } else if (isErrorStatus(error, 401)) {
        setError401(true);
      } else {
        axiosError(error);
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
          setConfirmed(true);
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
          />
          <Button
            variant="secondary"
            type="submit"
            disabled={!password.valid || !password2.valid}
          >
            Zmień hasło
          </Button>
        </Form>
      )}
    </AuthForbidden>
  );
};

export default SetPassword;
