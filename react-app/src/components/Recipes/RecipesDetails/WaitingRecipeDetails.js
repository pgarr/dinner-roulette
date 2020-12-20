import React from "react";
import { connect } from "react-redux";

import useFetchApi from "../../../shared/customHooks/useFetchApi";
import RecipeCard from "./RecipeCard/RecipeCard";
import RefusedBadge from "../../UI/RefusedBadge/RefusedBadge";
import LoadingContainer from "../../HOC/LoadingContainer/LoadingContainer";
import AuthRequired from "../../HOC/AuthRequired";
import { newPendingRecipe } from "../utils/baseRecipeObjects";

const WaitingRecipeDetails = ({ isAuthenticated, authToken, match }) => {
  const [{ data, isLoading }] = useFetchApi(
    {
      url: "/waiting/" + match.params.id,
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    },
    {
      pending_recipe: newPendingRecipe(),
    },
    isAuthenticated
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
