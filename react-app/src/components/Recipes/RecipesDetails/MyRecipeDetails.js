import React from "react";
import { connect } from "react-redux";
import { Button, Col, Row } from "react-bootstrap";

import useFetchApi from "../../../shared/customHooks/useFetchApi";
import LoadingContainer from "../../HOC/LoadingContainer/LoadingContainer";
import RecipeCard from "./RecipeCard/RecipeCard";
import AuthRequired from "../../HOC/AuthRequired";

const MyRecipeDetails = ({ isAuthenticated, authToken, match }) => {
  const [{ data, isLoading }] = useFetchApi(
    {
      url: "/recipes/" + match.params.id,
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    },
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
    },
    isAuthenticated
  );

  return (
    <AuthRequired>
      <LoadingContainer isLoading={isLoading}>
        <Row>
          <Col>
            <Button variant="primary">Edytuj</Button>
          </Col>
        </Row>
        <RecipeCard recipe={data.recipe} />
      </LoadingContainer>
    </AuthRequired>
  );
};

const mapStateToProps = (state) => {
  return {
    isAuthenticated: state.auth.access_token !== null,
    authToken: state.auth.access_token,
  };
};
export default connect(mapStateToProps)(MyRecipeDetails);
