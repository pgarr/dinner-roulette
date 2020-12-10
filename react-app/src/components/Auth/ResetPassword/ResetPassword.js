import React, { useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { Form, Button, Row, Col } from "react-bootstrap";

import { inputChangedHandler } from "../../../shared/handlers";
import axios from "../../../shared/axios-api";
import ModalWithBackdrop from "../../UI/ModalWithBackdrop/ModalWithBackdrop";
import { httpError } from "../../../shared/errors";

const ResetPassword = ({ isAuthenticated, authRedirectPath }) => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState(null); // TODO: reducer
  const [done, setDone] = useState(false); // TODO: reducer
  const [confirmed, setConfirmed] = useState(false); // TODO: reducer

  const submitHandler = async (event) => {
    event.preventDefault();

    // TODO: loading state (disabled form)
    try {
      const response = await axios.post("/auth/reset_password", {
        email,
      });
      switch (response.status) {
        case 202:
          setConfirmed(false);
          setDone(true);
          break;
        default:
          break;
      }
    } catch (error) {
      switch (error.response.status) {
        case 422:
          setError("Podany adres email nie jest zarejestrowany");
          break;
        default:
          httpError(error.response.status, error.response);
          break;
      }
    }
  };

  let redirect = null; // TODO: DRY problem, could be HOC
  if (isAuthenticated) {
    redirect = <Redirect to={authRedirectPath} />;
  }

  return (
    <React.Fragment>
      {redirect}

      <ModalWithBackdrop
        show={done && !confirmed}
        onHide={() => {
          setConfirmed(true);
          setDone(false);
        }}
        title="Sukces"
        text="Sprawdź swoją skrzynkę e-mail, aby zresetować hasło."
      />

      <h1>Zresetuj hasło</h1>
      <Form onSubmit={submitHandler}>
        <Form.Group as={Row} controlId="formEmail">
          <Form.Label column sm={12}>
            E-mail
          </Form.Label>
          <Col sm={12} md={6} lg={4}>
            <Form.Control
              required
              type="email"
              value={email}
              onChange={(event) => inputChangedHandler(event, setEmail)}
              isInvalid={error !== null}
            />
            <Form.Control.Feedback type="invalid">
              {error}
            </Form.Control.Feedback>
          </Col>
        </Form.Group>
        <Button variant="secondary" type="submit">
          {confirmed || done ? "Wyślij ponownie" : "Resetuj hasło"}
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

export default connect(mapStateToProps, null)(ResetPassword);
