import React from "react";
import { Form, Row, Col } from "react-bootstrap";

const InlineFormField = ({
  controlId,
  labelText,
  type,
  errors,
  value,
  onChangeHandler,
  isInvalid,
  isValid,
  disabled,
}) => {
  return (
    <Form.Group as={Row} controlId={controlId}>
      <Form.Label column sm={2}>
        {labelText}
      </Form.Label>
      <Col sm={10} md={8} lg={6}>
        <Form.Control
          required
          type={type}
          value={value}
          onChange={onChangeHandler}
          isInvalid={isInvalid}
          isValid={isValid}
          disabled={disabled}
        />
        <Form.Control.Feedback type="invalid">
          {errors[0]}
        </Form.Control.Feedback>
      </Col>
    </Form.Group>
  );
};

export default InlineFormField;
