import React from "react";
import { Button, Col, Form, InputGroup, Row } from "react-bootstrap";

import styles from "./IngredientsListForm.module.css";

const IngredientsListForm = ({
  ingredients,
  handleChange,
  handleAdd,
  handleRemove,
  disabled,
}) => {
  return (
    <React.Fragment>
      <Row>
        <Col lg={6} md={6} sm={6}>
          <Form.Label className={styles.IngredientLabel}>Nazwa</Form.Label>
        </Col>
        <Col lg={2} md={2} sm={2}>
          <Form.Label className={styles.IngredientLabel}>Ilość</Form.Label>
        </Col>
        <Col lg={2} md={2} sm={2}>
          <Form.Label className={styles.IngredientLabel}>Jednostka</Form.Label>
        </Col>
      </Row>
      {ingredients.map((ingredient) => {
        return (
          <InputGroup className="mb-1 ">
            <Form.Control
              type="text"
              value={ingredient.title}
              onChange={(event) =>
                handleChange(ingredient.id, { title: event.target.value })
              }
              disabled={disabled}
            />
            <Form.Control
              type="number"
              value={ingredient.amount}
              onChange={(event) =>
                handleChange(ingredient.id, { amount: event.target.value })
              }
              disabled={disabled}
            />
            <Form.Control
              type="text"
              value={ingredient.unit}
              onChange={(event) =>
                handleChange(ingredient.id, { unit: event.target.value })
              }
              disabled={disabled}
            />
            <InputGroup.Append>
              <Button
                variant="danger"
                onClick={(event) => {
                  handleRemove(ingredient.id);
                }}
                size="sm"
                disabled={disabled}
              >
                X
              </Button>
            </InputGroup.Append>
          </InputGroup>
        );
      })}
      <Row>
        <Col>
          <Button variant="success" onClick={handleAdd} disabled={disabled}>
            + składnik
          </Button>
        </Col>
      </Row>
    </React.Fragment>
  );
};

export default IngredientsListForm;
