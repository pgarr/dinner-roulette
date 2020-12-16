import React, { useState } from "react";
import { Form, Button, Row, Col } from "react-bootstrap";

import { inputChangedHandler } from "../../../shared/handlers";
import axios, { isErrorStatus } from "../../../shared/axios-api";
import ModalWithBackdrop from "../../UI/ModalWithBackdrop/ModalWithBackdrop";
import { axiosError } from "../../../shared/errors";
import AuthForbidden from "../../HOC/AuthForbidden";

const ResetPassword = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState(null); // TODO: reducer
  const [done, setDone] = useState(false);
  const [confirmed, setConfirmed] = useState(false);

  const submitHandler = async (event) => {
    event.preventDefault();

    // TODO: loading state (disabled form)
    try {
      await axios.post("/auth/reset_password", {
        email,
      });
      setConfirmed(false);
      setDone(true);
    } catch (error) {
      if (isErrorStatus(error, 422)) {
        setError("Podany adres email nie jest zarejestrowany");
      } else {
        axiosError(error);
      }
    }
  };

  return (
    <AuthForbidden>
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
    </AuthForbidden>
  );
};

export default ResetPassword;
