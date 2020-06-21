import React from "react";
import { Button, ButtonGroup, Col, Row } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import styles from "./RecipeCard.module.css";
import DifficultySymbol from "../UI/DifficultySymbol/DifficultySymbol";
import IngredientList from "./IngredientList/IngredientList";
import PreparationBox from "./PreparationBox/PreparationBox";

const RecipeCard = (props) => {
  return (
    <React.Fragment>
      <Row>
        <Col>
          <Button variant="primary">Edytuj</Button>{" "}
          <ButtonGroup aria-label="">
            <Button variant="success">Akceptuj</Button>
            <Button variant="danger">Odrzuć</Button>
          </ButtonGroup>
        </Col>
      </Row>
      <Row>
        <Col>
          <h2>{props.title}</h2>
        </Col>
      </Row>
      <Row>
        <Col>Autor: {props.author}</Col>
      </Row>
      <Row>
        <Col xs={2}>
          <FontAwesomeIcon icon="clock" />
          {props.time}'
        </Col>
        <Col xs={2}>
          <DifficultySymbol difficulty={props.difficulty} />
        </Col>
      </Row>
      <Row className={styles.Data}>
        <Col xs lg="4">
          {props.ingredients && (
            <IngredientList ingredients={props.ingredients} />
          )}
        </Col>
        <Col xs lg="8">
          {props.preparation && (
            <PreparationBox preparation={props.preparation} />
          )}
          {props.link && <a href={props.link}>Źródło</a>}
        </Col>
      </Row>
    </React.Fragment>
  );
};

export default RecipeCard;
