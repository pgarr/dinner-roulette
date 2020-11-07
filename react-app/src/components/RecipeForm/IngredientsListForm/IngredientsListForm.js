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
        <Col lg={6} md={6} sm={6}>
          <Form.Label>Nazwa</Form.Label>
        </Col>
        <Col lg={2} md={2} sm={2}>
          <Form.Label>Ilość</Form.Label>
        </Col>
        <Col lg={2} md={2} sm={2}>
          <Form.Label>Jednostka</Form.Label>
        </Col>
      </Row>
      {ingredients.map((ingredient) => {
        return (
          <Row key={ingredient.id}>
            <Col lg={6} md={6} sm={6}>
              <Form.Control
                type="text"
                value={ingredient.title}
                onChange={(event) =>
                  handleChange(ingredient.id, { title: event.target.value })
                }
              />
            </Col>
            <Col lg={2} md={2} sm={2}>
              <Form.Control
                type="text"
                value={ingredient.amount}
                onChange={(event) =>
                  handleChange(ingredient.id, { amount: event.target.value })
                }
              />
            </Col>
            <Col lg={2} md={2} sm={2}>
              <Form.Control
                type="text"
                value={ingredient.unit}
                onChange={(event) =>
                  handleChange(ingredient.id, { unit: event.target.value })
                }
              />
            </Col>
            <Col lg={2} md={2} sm={2}>
              <Button
                variant="danger"
                onClick={(event) => {
                  handleRemove(ingredient.id);
                }}
                size="sm"
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
