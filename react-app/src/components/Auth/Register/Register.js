import React, { useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { Form, Button, Row, Col } from "react-bootstrap";

import * as actions from "../../../store/actions/index";
import { inputChangedHandler } from "../../../shared/handlers";

const Register = ({ onRegister, isAuthenticated, authRedirectPath }) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [passwordsEqual, setPasswordsEqual] = useState(false);

  const submitHandler = (event) => {
    event.preventDefault();
    comparePasswords();
    if (passwordsEqual) {
      onRegister(username, password, email);
    }
  };

  const comparePasswords = () => {
    setPasswordsEqual(password === password2);
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
              value={username}
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
              value={email}
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
              value={password}
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
              value={password2}
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

const mapDispatchToProps = (dispatch) => {
  return {
    // onRegister: (username, password, email) =>
    //   dispatch(actions.register(username, password, email)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Register);
