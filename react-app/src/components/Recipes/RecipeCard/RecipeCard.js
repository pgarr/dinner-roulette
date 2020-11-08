import React, { useEffect, useState } from "react";
import { Button, ButtonGroup, Col, Row } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import axios from "../../../shared/axios-api";
import styles from "./RecipeCard.module.css";
import DifficultySymbol from "../../UI/DifficultySymbol/DifficultySymbol";
import IngredientList from "./IngredientList/IngredientList";
import PreparationBox from "./PreparationBox/PreparationBox";

const RecipeCard = ({ match }) => {
  const [recipe, setRecipe] = useState({
    author: "",
    difficulty: 0,
    ingredients: [],
    link: "",
    preparation: "",
    time: 0,
    title: "",
  });

  const [isLoading, setIsLoading] = useState(false); //TODO
  const [isError, setIsError] = useState(false); //TODO

  useEffect(() => {
    const fetchData = async () => {
      setIsError(false);
      setIsLoading(true);

      try {
        const response = await axios.get("/recipe/" + match.params.id);
        setRecipe(response.data.recipe);
      } catch (error) {
        console.log(error);
        setIsError(true);
      }
      setIsLoading(false);
    };

    fetchData();
  }, [match.params.id]);

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
          <h2>{recipe.title}</h2>
        </Col>
      </Row>
      <Row>
        <Col>Autor: {recipe.author}</Col>
      </Row>
      <Row>
        {recipe.time && (
          <Col xs={2}>
            <FontAwesomeIcon icon="clock" />
            {recipe.time}'
          </Col>
        )}
        {recipe.difficulty && (
          <Col xs={2}>
            <React.Fragment>
              <span>Trudność: </span>
              <DifficultySymbol difficulty={recipe.difficulty} />
            </React.Fragment>
          </Col>
        )}
      </Row>
      <Row className={styles.Data}>
        <Col xs lg="4">
          {recipe.ingredients && (
            <IngredientList ingredients={recipe.ingredients} />
          )}
        </Col>
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
