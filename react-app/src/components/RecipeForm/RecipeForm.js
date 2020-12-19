import React, { useState, useReducer } from "react";
import { Button, Col, Form, Row } from "react-bootstrap";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import RangeSlider from "react-bootstrap-range-slider";
import { v4 as uuidv4 } from "uuid";

import styles from "./RecipeForm.module.css";
import axios from "../../shared/axios-api";
import { inputChangedHandler } from "../../shared/handlers";
import IngredientsListForm from "./IngredientsListForm/IngredientsListForm";
import AuthRequired from "../HOC/AuthRequired";
import { axiosError } from "../../shared/errors";

const newIngredient = () => ({ id: uuidv4(), title: "", amount: "", unit: "" });

const ingredientReducer = (state, action) => {
  switch (action.type) {
    case "REMOVE":
      return state.filter((ingredient) => ingredient.id !== action.id);
    case "ADD":
      return state.concat(newIngredient());
    case "CHANGE":
      return state.map((ingredient) => {
        if (ingredient.id === action.id) {
          const updatedIngredient = { ...ingredient, ...action.changes };
          return updatedIngredient;
        }
        return ingredient;
      });
    default:
      return state;
  }
};

const RecipeForm = ({ authToken }) => {
  //form data
  const [title, setTitle] = useState("");
  const [time, setTime] = useState(0);
  const [difficulty, setDifficulty] = useState(0);
  const [ingredients, dispatchIngredients] = useReducer(ingredientReducer, [
    newIngredient(),
  ]);
  const [link, setLink] = useState("");
  const [preparation, setPreparation] = useState("");

  // component state
  const [pendingId, setPendingId] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAddIngredient = () => {
    dispatchIngredients({ type: "ADD" });
  };

  const handleRemoveIngredient = (id) => {
    dispatchIngredients({ type: "REMOVE", id });
  };

  const handleChange = (id, changes) => {
    dispatchIngredients({ type: "CHANGE", id, changes });
  };

  const submitHandler = async (event) => {
    event.preventDefault();

    setLoading(true);
    try {
      const response = await axios.post(
        "/recipe",
        {
          title,
          time,
          difficulty,
          ingredients,
          link,
          preparation,
        },
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );
      setPendingId(response.data.pending_recipe.id);
    } catch (error) {
      axiosError(error);
      setLoading(false);
    }
  };

  let redirect = null;
  if (pendingId) {
    redirect = <Redirect to={"/pendingrecipes/" + pendingId} />;
    //TODO toast
  }

  return (
    <AuthRequired>
      {redirect}
      <h1>Utwórz nowy przepis</h1>
      <Form onSubmit={submitHandler}>
        <Form.Group controlId="formTitle">
          <Form.Label>Nazwa przepisu</Form.Label>
          <Form.Control
            required
            type="text"
            value={title}
            onChange={(event) => inputChangedHandler(event, setTitle)}
            disabled={loading}
          />
        </Form.Group>
        <Row className={styles.TopForm}>
          <Col lg={4}>
            <Form.Group controlId="formTime">
              <Form.Label>Czas przygotowania (minuty)</Form.Label>
              <RangeSlider
                type="range"
                value={time}
                onChange={(event) => inputChangedHandler(event, setTime)}
                variant="info"
                tooltipPlacement="bottom"
                tooltip="on"
                min={0}
                max={180}
                step={5}
                disabled={loading}
              />
            </Form.Group>
          </Col>
          <Col lg={4}>
            <Form.Group controlId="formDifficulty">
              <Form.Label>Trudność przygotowania (1-5)</Form.Label>
              <Form.Control
                type="text"
                value={difficulty}
                onChange={(event) => inputChangedHandler(event, setDifficulty)}
                disabled={loading}
              />
            </Form.Group>
          </Col>
        </Row>
        <Row>
          <Col lg={6} sm={12}>
            <h2>Składniki</h2>
            <IngredientsListForm
              ingredients={ingredients}
              handleChange={handleChange}
              handleAdd={handleAddIngredient}
              handleRemove={handleRemoveIngredient}
              disabled={loading}
            />
          </Col>
          <Col lg={6} sm={12}>
            <Form.Group controlId="formPrep">
              <Form.Label>Przygotowanie</Form.Label>
              <Form.Control
                required
                type="text"
                as="textarea"
                rows={10}
                value={preparation}
                onChange={(event) => inputChangedHandler(event, setPreparation)}
                disabled={loading}
              />
            </Form.Group>
            <Form.Group controlId="formSource">
              <Form.Label>Źródło</Form.Label>
              <Form.Control
                type="text"
                value={link}
                onChange={(event) => inputChangedHandler(event, setLink)}
                disabled={loading}
              />
            </Form.Group>
          </Col>
        </Row>
        <Button variant="secondary" type="submit" disabled={loading}>
          Zapisz
        </Button>
      </Form>
    </AuthRequired>
  );
};

const mapStateToProps = (state) => {
  return {
    authToken: state.auth.access_token,
  };
};

export default connect(mapStateToProps)(RecipeForm);
