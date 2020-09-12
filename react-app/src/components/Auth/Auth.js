import React, { useEffect, useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";

import * as actions from "../../store/actions/index";
import { Form, Button, Row, Col } from "react-bootstrap";

const Auth = ({
  loading,
  error,
  isAuthenticated,
  authRedirectPath,
  onAuth,
}) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const inputChangedHandler = (event, setValue) => {
    setValue(event.target.value);
  };

  const submitHandler = (event) => {
    event.preventDefault();
    onAuth(username, password);
  };

  let errorMessage = null;
  if (error) {
    errorMessage = <p>{error.description}</p>;
  }

  let authRedirect = null;
  if (isAuthenticated) {
    authRedirect = <Redirect to={authRedirectPath} />;
  }

  return (
    <React.Fragment>
      {authRedirect}
      <h1>Zaloguj się</h1>
      {errorMessage}
      <Form onSubmit={submitHandler}>
        <Form.Group as={Row} controlId="formUsername">
          <Form.Label column sm={12}>
            Nazwa użytkownika
          </Form.Label>
          <Col sm={12} md={6} lg={4}>
            <Form.Control
              required
              type="text"
              value={username}
              onChange={(event) => inputChangedHandler(event, setUsername)}
            />
          </Col>
        </Form.Group>

        <Form.Group as={Row} controlId="formPassword">
          <Form.Label column sm={12}>
            Hasło
          </Form.Label>
          <Col sm={12} md={6} lg={4}>
            <Form.Control
              required
              type="password"
              value={[password]}
              onChange={(event) => inputChangedHandler(event, setPassword)}
            />
          </Col>
        </Form.Group>
        <Form.Group controlId="formRememberCheckbox">
          <Form.Check type="checkbox" label="Zapamiętaj mnie" />
        </Form.Group>
        <Button variant="secondary" type="submit">
          Zaloguj się
        </Button>
      </Form>
    </React.Fragment>
  );
};

const mapStateToProps = (state) => {
  return {
    loading: state.auth.loading,
    error: state.auth.error,
    isAuthenticated: state.auth.token !== null,
    authRedirectPath: state.auth.authRedirectPath,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onAuth: (username, password) => dispatch(actions.auth(username, password)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Auth);