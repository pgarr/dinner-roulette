import React, { useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { Form, Button } from "react-bootstrap";

import {
  validateOnBackend,
  validatePassword,
  validatePassword2,
} from "./validators";
import { useDebouncedEffect } from "../../../shared/customHooks";
import RegisterFormField from "./RegisterFormField";

const Register = ({ isAuthenticated, authRedirectPath }) => {
  const [validated, setValidated] = useState(false);

  const [username, setUsername] = useState({ value: "", touched: false });
  const [usernameValidation, setUsernameValidation] = useState({
    valid: false,
    errors: [],
  });
  const [email, setEmail] = useState({ value: "", touched: false });
  const [emailValidation, setEmailValidation] = useState({
    valid: false,
    errors: [],
  });
  const [password, setPassword] = useState({ value: "", touched: false });
  const [passwordValidation, setPasswordValidation] = useState({
    valid: false,
    errors: [],
  });
  const [password2, setPassword2] = useState({ value: "", touched: false });
  const [password2Validation, setPassword2Validation] = useState({
    valid: false,
    errors: [],
  });

  const validationDelay = 1000;

  const inputChangedHandler = (event, setValue) => {
    setValue({ value: event.target.value, touched: true });
  };

  // validate username and email
  useDebouncedEffect(
    async () => {
      let usernameParam = null;
      let emailParam = null;

      if (username.touched) {
        usernameParam = username.value;
      }
      if (email.touched) {
        emailParam = email.value;
      }

      if (usernameParam !== null || emailParam !== null) {
        const result = await validateOnBackend(usernameParam, emailParam);
        for (const key in result) {
          switch (key) {
            case "username":
              setUsernameValidation({ ...usernameValidation, ...result[key] });
              break;
            case "email":
              setEmailValidation({ ...emailValidation, ...result[key] });
              break;
            default:
              break;
          }
        }
      }
    },
    validationDelay,
    [username, email]
  );

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

  const submitHandler = (event) => {
    event.preventDefault();
    // if (passwordsEqual) {
    //   onRegister(username, password, email);
    // }
  };

  let authRedirect = null;
  if (isAuthenticated) {
    authRedirect = <Redirect to={authRedirectPath} />;
  }

  return (
    <React.Fragment>
      {authRedirect}
      <h1>Zarejestruj się</h1>
      <Form noValidate validated={validated} onSubmit={submitHandler}>
        <RegisterFormField
          controlId="formUsername"
          labelText="Nazwa użytkownika"
          type="text"
          errors={usernameValidation.errors}
          value={username.value}
          onChangeHandler={(event) => {
            inputChangedHandler(event, setUsername);
          }}
          isValid={username.touched && usernameValidation.valid}
          isInvalid={username.touched && !usernameValidation.valid}
        />
        <RegisterFormField
          controlId="formEmail"
          labelText="E-mail"
          type="email"
          errors={emailValidation.errors}
          value={email.value}
          onChangeHandler={(event) => {
            inputChangedHandler(event, setEmail);
          }}
          isValid={email.touched && emailValidation.valid}
          isInvalid={email.touched && !emailValidation.valid}
        />
        <RegisterFormField
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
        <RegisterFormField
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
        <Button variant="secondary" type="submit">
          Zarejestruj się
        </Button>
      </Form>
    </React.Fragment>
  );
};

const mapStateToProps = (state) => {
  return {
    isAuthenticated: state.auth.access_token !== null,
    authRedirectPath: state.auth.authRedirectPath,
  };
};

export default connect(mapStateToProps, null)(Register);
