import React, { useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { Form, Button } from "react-bootstrap";

import {
  validatePassword,
  validatePassword2,
  buildValidationObject,
} from "../Register/validators";
import { isExpired } from "../../../shared/tokenDecode";
import axios from "../../../shared/axios-api";
import { inputTouchedChangedHandler as inputChangedHandler } from "../../../shared/handlers";
import useDebouncedEffect from "../../../shared/customHooks/useDebouncedEffect";
import ModalWithBackdrop from "../../UI/ModalWithBackdrop/ModalWithBackdrop";
import InlineFormField from "../../UI/InlineFormField/InlineFormField";
import { httpError } from "../../../shared/errors";

const SetPassword = ({ authRedirectPath, isAuthenticated, match }) => {
  const [validated, setValidated] = useState(false); // TODO useReducer
  const [changed, setChanged] = useState(false);
  const [confirmed, setConfirmed] = useState(false);
  const [error401, setError401] = useState(false);

  const [password, setPassword] = useState({ value: "", touched: false }); // TODO useReducer
  const [passwordValidation, setPasswordValidation] = useState({
    valid: false,
    errors: [],
  });
  const [password2, setPassword2] = useState({ value: "", touched: false }); // TODO useReducer
  const [password2Validation, setPassword2Validation] = useState({
    valid: false,
    errors: [],
  });

  const validationDelay = 1000;

  // validate password
  useDebouncedEffect(
    () => {
      if (password.touched) {
        const result = validatePassword(password.value);
        setPasswordValidation({ ...passwordValidation, ...result });
      }
    },
    validationDelay,
    [password]
  );

  // validate password2
  useDebouncedEffect(
    () => {
      if (password2.touched) {
        const result = validatePassword2(password.value, password2.value);
        setPassword2Validation({ ...password2Validation, ...result });
      }
    },
    validationDelay,
    [password2]
  );

  const submitHandler = async (event) => {
    event.preventDefault();

    // TODO: loading state (disabled form)
    try {
      const response = await axios.post(
        "/auth/reset_password/" + match.params.token,
        {
          password: password.value,
        }
      );
      setValidated(true);

      switch (response.status) {
        case 200:
          setChanged(true);
          break;
        default:
          break;
      }
    } catch (error) {
      setValidated(false);
      switch (error.response.status) {
        case 422:
          const result = buildValidationObject(error.response.data);
          setPasswordValidation({ ...passwordValidation, ...result.password });
          break;
        case 401:
          setError401(true);
          break;
        default:
          httpError(error.response.status, error.response);
          break;
      }
    }
  };

  let redirect = null;
  if (isAuthenticated) {
    redirect = <Redirect to={authRedirectPath} />;
  } else if (confirmed) {
    redirect = <Redirect to={"/login"} />;
  }

  return (
    <React.Fragment>
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
            errors={passwordValidation.errors}
            value={password.value}
            onChangeHandler={(event) => {
              inputChangedHandler(event, setPassword);
            }}
            isValid={password.touched && passwordValidation.valid}
            isInvalid={password.touched && !passwordValidation.valid}
          />
          <InlineFormField
            controlId="formPassword2"
            labelText="Powtórz hasło"
            type="password"
            errors={password2Validation.errors}
            value={password2.value}
            onChangeHandler={(event) => {
              inputChangedHandler(event, setPassword2);
            }}
            isValid={password2.touched && password2Validation.valid}
            isInvalid={password2.touched && !password2Validation.valid}
          />
          <Button
            variant="secondary"
            type="submit"
            disabled={!passwordValidation.valid || !password2Validation.valid}
          >
            Zmień hasło
          </Button>
        </Form>
      )}
    </React.Fragment>
  );
};

const mapStateToProps = (state) => {
  return {
    isAuthenticated: state.auth.access_token !== null,
    authRedirectPath: state.auth.authRedirectPath,
  };
};

export default connect(mapStateToProps, null)(SetPassword);
