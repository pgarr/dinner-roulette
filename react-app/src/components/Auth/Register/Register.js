import React, { useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { Form, Button, Row, Col } from "react-bootstrap";

import { inputChangedHandler } from "../../../shared/handlers";
import { validateUsername } from "./validators";
import { useDebouncedEffect } from "../../../shared/customHooks";

const Register = ({ isAuthenticated, authRedirectPath }) => {
  const [username, setUsername] = useState({ value: "", touched: false });
  const [usernameValidation, setUsernameValidation] = useState({
    valid: false,
    validator: validateUsername,
    error: "",
  });
  const [email, setEmail] = useState({ value: "", touched: false });
  const [emailValidation, setEmailValidation] = useState({
    valid: false,
    validator: () => {},
    error: "",
  });
  const [password, setPassword] = useState({ value: "", touched: false });
  const [passwordValidation, setPasswordValidation] = useState({
    valid: false,
    validator: () => {},
    error: "",
  });
  const [password2, setPassword2] = useState({ value: "", touched: false });
  const [password2Validation, setPassword2Validation] = useState({
    valid: false,
    validator: () => {},
    error: "",
  });

  const validationDelay = 1000;

  const inputChangedHandler = (event, setValue) => {
    setValue({ value: event.target.value, touched: true });
  };

  // validate username
  useDebouncedEffect(
    async () => {
      if (username.touched) {
        const result = await validateUsername(username.value);
        setUsernameValidation({ ...usernameValidation, ...result });
        console.log(result);
      }
    },
    validationDelay,
    [username]
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
      <Form onSubmit={submitHandler}>
        <Form.Group as={Row} controlId="formUsername">
          <Form.Label column sm={2}>
            Nazwa użytkownika
          </Form.Label>
          <Col sm={10} md={8} lg={6}>
            <Form.Control
              required
              type="text"
              value={username.value}
              onChange={(event) => inputChangedHandler(event, setUsername)}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} controlId="formEmail">
          <Form.Label column sm={2}>
            E-mail
          </Form.Label>
          <Col sm={10} md={8} lg={6}>
            <Form.Control
              required
              type="email"
              value={email.value}
              onChange={(event) => inputChangedHandler(event, setEmail)}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} controlId="formPassword">
          <Form.Label column sm={2}>
            Hasło
          </Form.Label>
          <Col sm={10} md={8} lg={6}>
            <Form.Control
              required
              type="password"
              value={password.value}
              onChange={(event) => inputChangedHandler(event, setPassword)}
            />
          </Col>
        </Form.Group>
        <Form.Group as={Row} controlId="formPassword2">
          <Form.Label column sm={2}>
            Powtórz hasło
          </Form.Label>
          <Col sm={10} md={8} lg={6}>
            <Form.Control
              required
              type="password"
              value={password2.value}
              onChange={(event) => inputChangedHandler(event, setPassword2)}
            />
          </Col>
        </Form.Group>
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
