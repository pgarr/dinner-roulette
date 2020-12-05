import React from "react";
// import { Button, ButtonGroup, Col, Row } from "react-bootstrap";

import useFetchApi from "../../../shared/customHooks/useFetchApi";
import LoadingContainer from "../../HOC/LoadingContainer/LoadingContainer";
import RecipeCard from "./RecipeCard/RecipeCard";

const RecipeDetails = ({ match }) => {
  const [{ data, isLoading, isError }] = useFetchApi(
    { url: "/recipe/" + match.params.id },
    {
      recipe: {
        author: "",
        difficulty: 0,
        ingredients: [],
        link: "",
        preparation: "",
        time: 0,
        title: "",
      },
    }
  );

  return (
    <LoadingContainer isLoading={isLoading}>
      {/* <Row>
        <Col>
          <Button variant="primary">Edytuj</Button>{" "}
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
