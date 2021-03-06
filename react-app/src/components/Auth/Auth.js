import React, { useState } from "react";
import { connect } from "react-redux";
import { Form, Button, Row, Col } from "react-bootstrap";

import { inputChangedHandler } from "../../shared/handlers";
import styles from "./Auth.module.css";
import * as actions from "../../store/actions/index";
import AuthForbidden from "../HOC/AuthForbidden";

const Auth = ({ loading, error, onAuth }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const submitHandler = (event) => {
    event.preventDefault();
    onAuth(username, password);
  };

  return (
    <AuthForbidden>
      <h1>Zaloguj się</h1>
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
              disabled={loading}
              isInvalid={error !== null}
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
              value={password}
              onChange={(event) => inputChangedHandler(event, setPassword)}
              disabled={loading}
              isInvalid={error !== null}
            />
            <Form.Control.Feedback type="invalid">
              {error}
            </Form.Control.Feedback>
          </Col>
        </Form.Group>
        <Button variant="secondary" type="submit" disabled={loading}>
          {loading ? "Wczytuję..." : "Zaloguj się"}
        </Button>
        <div className={styles.ButtonsRow}>
          <Button href="/register" variant="outline-info" disabled={loading}>
            Nowy użytkownik?
          </Button>
          <Button
            href="/resetrequest"
            variant="outline-info"
            disabled={loading}
          >
            Zapomniałeś hasła?
          </Button>
        </div>
      </Form>
    </AuthForbidden>
  );
};

const mapStateToProps = (state) => {
  return {
    loading: state.auth.loading,
    error: state.auth.error,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onAuth: (username, password) => dispatch(actions.auth(username, password)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Auth);
