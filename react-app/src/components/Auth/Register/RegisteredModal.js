import React from "react";
import { Button, Modal } from "react-bootstrap";

const RegisteredModal = ({ show, onHide }) => {
  return (
    <Modal show={show} onHide={onHide} backdrop="static" keyboard={false}>
      <Modal.Header closeButton>
        <Modal.Title>Sukces!</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        Zarejestrowałeś się. Zaloguj się za pomocą podanych danych.
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Ok
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default RegisteredModal;
