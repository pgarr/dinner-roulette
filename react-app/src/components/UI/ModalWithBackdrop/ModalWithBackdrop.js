import React from "react";
import { Button, Modal } from "react-bootstrap";

const ModalWithBackdrop = ({ show, onHide, title, text }) => {
  return (
    <Modal show={show} onHide={onHide} backdrop="static" keyboard={false}>
      <Modal.Header closeButton>
        <Modal.Title>{title}</Modal.Title>
      </Modal.Header>
      <Modal.Body>{text}</Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Ok
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalWithBackdrop;
