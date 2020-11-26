import React, { useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { Form, Button, Row, Col } from "react-bootstrap";

import { inputChangedHandler } from "../../../shared/handlers";
import axios from "../../../shared/axios-api";
import ModalWithBackdrop from "../../UI/ModalWithBackdrop/ModalWithBackdrop";

const ResetPassword = ({ isAuthenticated, authRedirectPath }) => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState(null);
  const [done, setDone] = useState(false);
  const [confirmed, setConfirmed] = useState(false);

  const submitHandler = async (event) => {
    event.preventDefault();

    // TODO: loading state (disabled form)
    try {
      const response = await axios.post("/auth/reset_password_request", {
        email,
      });

      if (response.status === 202) {
        setDone(true);
      } else {
        console.log(response); // TODO
      }
    } catch (error) {
      if (error.response.status === 422) {
        setError("Podany adres email nie jest zarejestrowany");
      } else {
        console.log(error.response); // TODO
      }
    }
  };

  let redirect = null; // TODO: DRY problem, could be HOC
  if (isAuthenticated) {
    redirect = <Redirect to={authRedirectPath} />;
  } else if (confirmed) {
    redirect = <Redirect to={"/login"} />;
  }

  return (
    <React.Fragment>
      {redirect}

      <ModalWithBackdrop
        show={done && !confirmed}
        onHide={() => {
          setConfirmed(true);
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
          Resetuj hasło
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
