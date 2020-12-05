import React from "react";
import { connect } from "react-redux";

import useFetchApi from "../../../shared/customHooks/useFetchApi";
import RecipeCard from "./RecipeCard/RecipeCard";
import RefusedBadge from "../../UI/RefusedBadge/RefusedBadge";
import LoadingContainer from "../../UI/LoadingContainer/LoadingContainer";
import AuthRequired from "../../HOC/AuthRequired";

const WaitingRecipeDetails = ({ isAuthenticated, authToken, match }) => {
  const [{ data, isLoading, isError }] = useFetchApi(
    {
      url: "/waiting/" + match.params.id,
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    },
    {
      pending_recipe: {
        author: "",
        difficulty: 0,
        ingredients: [],
        link: "",
        preparation: "",
        time: 0,
        title: "",
        refused: false,
      },
      isAuthenticated,
    }
  );

  return (
    <AuthRequired>
      <LoadingContainer isLoading={isLoading}>
        <RefusedBadge refused={data.pending_recipe.refused} />
        <RecipeCard recipe={data.pending_recipe} />
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

export default connect(mapStateToProps)(WaitingRecipeDetails);
