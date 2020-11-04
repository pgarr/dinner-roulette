import { faRainbow } from "@fortawesome/free-solid-svg-icons";
import React from "react";
import { Button, Col, Form, Row } from "react-bootstrap";

const IngredientsListForm = ({
  ingredients,
  handleChange,
  handleAdd,
  handleRemove,
}) => {
  return (
    <React.Fragment>
      <Row>
        <Col lg={6}>
          <Form.Label>Nazwa</Form.Label>
        </Col>
        <Col lg={2}>
          <Form.Label>Ilość</Form.Label>
        </Col>
        <Col lg={2}>
          <Form.Label>Jednostka</Form.Label>
        </Col>
      </Row>
      {ingredients.map((ingredient) => {
        return (
          <Row key={ingredient.id}>
            <Col lg={6}>
              <Form.Control
                type="text"
                value={ingredient.name}
                onChange={(event) =>
                  handleChange(ingredient.id, { name: event.target.value })
                }
              />
            </Col>
            <Col lg={2}>
              <Form.Control
                type="text"
                value={ingredient.amount}
                onChange={(event) =>
                  handleChange(ingredient.id, { amount: event.target.value })
                }
              />
            </Col>
            <Col lg={2}>
              <Form.Control
                type="text"
                value={ingredient.unit}
                onChange={(event) =>
                  handleChange(ingredient.id, { unit: event.target.value })
                }
              />
            </Col>
            <Col lg={2}>
              <Button
                variant="danger"
                onClick={(event) => {
                  handleRemove(ingredient.id);
                }}
              >
                X
              </Button>
            </Col>
          </Row>
        );
      })}
      <Row>
        <Col>
          <Button variant="success" onClick={handleAdd}>
            + składnik
          </Button>
        </Col>
      </Row>
    </React.Fragment>
  );
};

export default IngredientsListForm;
