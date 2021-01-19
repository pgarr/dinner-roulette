import React from "react";
import { Col, Row } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import styles from "./RecipeCard.module.css";
import DifficultySymbol from "../../../UI/DifficultySymbol/DifficultySymbol";
import IngredientList from "./IngredientList/IngredientList";
import PreparationBox from "./PreparationBox/PreparationBox";

const RecipeCard = ({ recipe }) => {
  return (
    <React.Fragment>
      <Row>
        <Col>
          <h2>{recipe.title}</h2>
        </Col>
      </Row>
      <Row>
        <Col>Autor: {recipe.author}</Col>
      </Row>
      <Row>
        {recipe.time ? (
          <Col xs={2}>
            <FontAwesomeIcon icon="clock" /> {recipe.time}'
          </Col>
        ) : null}
        {recipe.difficulty ? (
          <Col xs={2}>
            <React.Fragment>
              <span>Trudność: </span>
              <DifficultySymbol difficulty={recipe.difficulty} />
            </React.Fragment>
          </Col>
        ) : null}
      </Row>
      <Row className={styles.Data}>
        {recipe.ingredients.length > 0 ? (
          <Col xs lg="4">
            <IngredientList ingredients={recipe.ingredients} />
          </Col>
        ) : null}
        <Col xs lg="8">
          {recipe.preparation && (
            <PreparationBox preparation={recipe.preparation} />
          )}
          {recipe.link && <a href={recipe.link}>Źródło</a>}
        </Col>
      </Row>
    </React.Fragment>
  );
};

export default RecipeCard;
