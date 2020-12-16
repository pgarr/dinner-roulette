import React, { useReducer, useState } from "react";
import { Form, Button, Row, Col } from "react-bootstrap";

import { inputChangedHandler } from "../../../shared/handlers";
import axios, { isErrorStatus } from "../../../shared/axios-api";
import ModalWithBackdrop from "../../UI/ModalWithBackdrop/ModalWithBackdrop";
import { axiosError } from "../../../shared/errors";
import AuthForbidden from "../../HOC/AuthForbidden";

const resetReducer = (state, action) => {
  switch (action.type) {
    case "INIT_REQUEST":
      return {
        ...state,
        error422: false,
        done: false,
        confirmed: false,
        loading: true,
      };
    case "REQUEST_SUCCESS":
      return { ...state, error: false, done: true, loading: false };
    case "REQUEST_FAIL":
      return { ...state, loading: false };
    case "ERROR_422":
      return { ...state, error422: true };
    case "MODAL_CONFIRMED":
      return { ...state, confirmed: true };
    default:
      return { ...state };
  }
};

const ResetPassword = () => {
  const [email, setEmail] = useState("");
  const [{ error422, done, confirmed, loading }, dispatch] = useReducer(
    resetReducer,
    {
      error422: false,
      done: false,
      confirmed: false,
      loading: false,
    }
  );

  const submitHandler = async (event) => {
    event.preventDefault();
    dispatch({ type: "INIT_REQUEST" });
    try {
      await axios.post("/auth/reset_password", {
        email,
      });
      dispatch({ type: "REQUEST_SUCCESS" });
    } catch (error) {
      if (isErrorStatus(error, 422)) {
        dispatch({ type: "ERROR_422" });
      } else {
        axiosError(error);
      }
      dispatch({ type: "REQUEST_FAIL" });
    }
  };

  return (
    <AuthForbidden>
      <ModalWithBackdrop
        show={done && !confirmed}
        onHide={() => {
          dispatch({ type: "MODAL_CONFIRMED" });
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
              isInvalid={error422}
              disabled={loading}
            />
            <Form.Control.Feedback type="invalid">
              {"Podany adres email nie jest zarejestrowany"}
            </Form.Control.Feedback>
          </Col>
        </Form.Group>
        <Button variant="secondary" type="submit" disabled={loading}>
          {confirmed || done ? "Wyślij ponownie" : "Resetuj hasło"}
        </Button>
      </Form>
    </AuthForbidden>
  );
};

export default ResetPassword;
