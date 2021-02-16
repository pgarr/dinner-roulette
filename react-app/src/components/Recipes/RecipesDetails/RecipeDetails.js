import React from "react";
// import { Button, ButtonGroup, Col, Row } from "react-bootstrap";

import useFetchApi from "../../../shared/customHooks/useFetchApi";
import LoadingContainer from "../../HOC/LoadingContainer/LoadingContainer";
import { newRecipe } from "../utils/baseRecipeObjects";
import RecipeCard from "./RecipeCard/RecipeCard";

const RecipeDetails = ({ match }) => {
  const [{ data, isLoading }] = useFetchApi(
    { url: "/recipes/" + match.params.id },
    {
      recipe: newRecipe(),
    }
  );

  return (
    <LoadingContainer isLoading={isLoading}>
      {/* <Row>
        <Col>
          <ButtonGroup aria-label="">
            <Button variant="success">Akceptuj</Button>
            <Button variant="danger">Odrzuć</Button>
          </ButtonGroup>
        </Col>
      </Row> */}
      <RecipeCard recipe={data.recipe} />
    </LoadingContainer>
  );
};

export default RecipeDetails;
