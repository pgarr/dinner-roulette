import React, { useState, useEffect } from "react";
import { Button, ButtonGroup, Col, Row } from "react-bootstrap";

import axios from "../../../shared/axios-api";
import RecipeCard from "./RecipeCard/RecipeCard";

const RecipeDetails = ({ match }) => {
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
      {/* <Row>
        <Col>
          <Button variant="primary">Edytuj</Button>{" "}
          <ButtonGroup aria-label="">
            <Button variant="success">Akceptuj</Button>
            <Button variant="danger">Odrzuć</Button>
          </ButtonGroup>
        </Col>
      </Row> */}
      <RecipeCard recipe={recipe} />;
    </React.Fragment>
  );
};

export default RecipeDetails;
