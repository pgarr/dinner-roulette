import React from "react";
import { Button, Col, Form, Row } from "react-bootstrap";
import RangeSlider from "react-bootstrap-range-slider";

import styles from "./RecipeForm.module.css";
import IngredientsListForm from "./IngredientsListForm/IngredientsListForm";
import DifficultyPicker from "../../../UI/DifficultyPicker/DifficultyPicker";

const RecipeForm = ({ dispatchRecipe, loading, onSubmit, recipe }) => {
  return (
    <Form onSubmit={onSubmit}>
      <Row className={styles.TopForm}>
        <Col md={6}>
          <Form.Group controlId="formTitle">
            <Form.Label>Tytuł</Form.Label>
            <Form.Control
              required
              type="text"
              value={recipe.title}
              onChange={(event) =>
                dispatchRecipe({
                  type: "CHANGE",
                  data: { title: event.target.value },
                })
              }
              disabled={loading}
            />
          </Form.Group>
          <Form.Group controlId="formTime">
            <Form.Label>Czas (minuty)</Form.Label>
            <RangeSlider
              type="range"
              value={recipe.time}
              onChange={(event) =>
                dispatchRecipe({
                  type: "CHANGE",
                  data: { time: event.target.value },
                })
              }
              variant="info"
              tooltipPlacement="bottom"
              tooltip="on"
              min={0}
              max={180}
              step={5}
              disabled={loading}
            />
          </Form.Group>
          <Form.Group controlId="formDifficulty">
            <Form.Label>Poziom trudności</Form.Label>
            <DifficultyPicker
              onChange={(value) =>
                dispatchRecipe({
                  type: "CHANGE",
                  data: { difficulty: value },
                })
              }
              initialValue={recipe.difficulty}
              disabled={loading}
            />
          </Form.Group>
        </Col>
        <Col lg={6}>
          <h2>Składniki</h2>
          <IngredientsListForm
            ingredients={recipe.ingredients}
            handleChange={(id, changes) => {
              dispatchRecipe({ type: "CHANGE_INGREDIENT", id, changes });
            }}
            handleAdd={() => {
              dispatchRecipe({ type: "ADD_INGREDIENT" });
            }}
            handleRemove={(id) => {
              dispatchRecipe({ type: "REMOVE_INGREDIENT", id });
            }}
            disabled={loading}
          />
        </Col>
      </Row>
      <Row>
        <Col>
          <Form.Group controlId="formPrep">
            <Form.Label>Przygotowanie</Form.Label>
            <Form.Control
              required
              type="text"
              as="textarea"
              rows={10}
              value={recipe.preparation}
              onChange={(event) =>
                dispatchRecipe({
                  type: "CHANGE",
                  data: { preparation: event.target.value },
                })
              }
              disabled={loading}
            />
          </Form.Group>
          <Form.Group controlId="formSource">
            <Form.Label>Źródło</Form.Label>
            <Form.Control
              type="text"
              value={recipe.link}
              onChange={(event) =>
                dispatchRecipe({
                  type: "CHANGE",
                  data: { link: event.target.value },
                })
              }
              disabled={loading}
            />
          </Form.Group>
        </Col>
      </Row>
      <Button variant="secondary" type="submit" disabled={loading}>
        Zapisz
      </Button>
    </Form>
  );
};

export default RecipeForm;
