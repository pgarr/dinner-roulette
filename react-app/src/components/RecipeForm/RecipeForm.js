import React, { useState, useReducer } from "react";
import { Col, Form, Row } from "react-bootstrap";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { v4 as uuidv4 } from "uuid";

import { inputChangedHandler } from "../../shared/handlers";
import * as actions from "../../store/actions/index";
import IngredientsListForm from "./IngredientsListForm";

const newIngredient = () => ({ id: uuidv4(), name: "", amount: "", unit: "" });

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

const RecipeForm = ({ isAuthenticated, onSetAuthRedirectPath }) => {
  const [title, setTitle] = useState("");
  const [time, setTime] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [ingredients, dispatchIngredients] = useReducer(ingredientReducer, [
    newIngredient(),
  ]);
  const [source, setSource] = useState("");
  const [preparation, setPreparation] = useState("");

  const handleAddIngredient = () => {
    dispatchIngredients({ type: "ADD" });
  };

  const handleRemoveIngredient = (id) => {
    dispatchIngredients({ type: "REMOVE", id });
  };

  const handleChange = (id, changes) => {
    dispatchIngredients({ type: "CHANGE", id, changes });
  };

  const submitHandler = () => {
    //TODO
  };

  let redirect = null;
  if (!isAuthenticated) {
    redirect = <Redirect to={"/login"} />;
    onSetAuthRedirectPath("/newrecipe");
  }

  return (
    <React.Fragment>
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
          />
        </Form.Group>
        <Row>
          <Col lg={4}>
            <Form.Group controlId="formTime">
              <Form.Label>Czas przygotowania (minuty)</Form.Label>
              <Form.Control
                type="text"
                value={time}
                onChange={(event) => inputChangedHandler(event, setTime)}
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
              />
            </Form.Group>
          </Col>
        </Row>
        <h2>Składniki</h2>
        <IngredientsListForm
          ingredients={ingredients}
          handleChange={handleChange}
          handleAdd={handleAddIngredient}
          handleRemove={handleRemoveIngredient}
        />
      </Form>
    </React.Fragment>
  );
};

const mapStateToProps = (state) => {
  return {
    isAuthenticated: state.auth.access_token !== null,
    authRedirectPath: state.auth.authRedirectPath,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onSetAuthRedirectPath: (path) =>
      dispatch(actions.setAuthRedirectPath(path)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(RecipeForm);
