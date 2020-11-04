import React, { useEffect } from "react";
import { connect } from "react-redux";
import { Button, ButtonGroup, Col, Row } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import styles from "./RecipeCard.module.css";
import DifficultySymbol from "../UI/DifficultySymbol/DifficultySymbol";
import IngredientList from "./IngredientList/IngredientList";
import PreparationBox from "./PreparationBox/PreparationBox";
import * as actions from "../../store/actions/index";

// TODO: remove redux, just useState for component
const RecipeCard = ({
  title,
  author,
  time,
  difficulty,
  ingredients,
  preparation,
  link,
  loading,
  onLoadDetails,
  match,
}) => {
  useEffect(() => {
    onLoadDetails(match.params.id);
  }, [match.params.id, onLoadDetails]);

  let diff = null;
  if (difficulty) {
    diff = (
      <React.Fragment>
        <span>Trudność: </span>
        <DifficultySymbol difficulty={difficulty} />
      </React.Fragment>
    );
  }

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
          <h2>{title}</h2>
        </Col>
      </Row>
      <Row>
        <Col>Autor: {author}</Col>
      </Row>
      <Row>
        {time && (
          <Col xs={2}>
            <FontAwesomeIcon icon="clock" />
            {time}'
          </Col>
        )}
        {diff && <Col xs={2}>{diff}</Col>}
      </Row>
      <Row className={styles.Data}>
        <Col xs lg="4">
          {ingredients && <IngredientList ingredients={ingredients} />}
        </Col>
        <Col xs lg="8">
          {preparation && <PreparationBox preparation={preparation} />}
          {link && <a href={link}>Źródło</a>}
        </Col>
      </Row>
    </React.Fragment>
  );
};

const mapStateToProps = (state) => {
  return {
    title: state.details.title,
    author: state.details.author,
    time: state.details.time,
    difficulty: state.details.difficulty,
    ingredients: state.details.ingredients,
    preparation: state.details.preparation,
    link: state.details.link,
    loading: state.details.loading,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onLoadDetails: (id) => dispatch(actions.loadDetails(id)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(RecipeCard);
