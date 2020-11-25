import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";

import useFetchApi from "../../../shared/customHooks/useFetchApi";
import * as actions from "../../../store/actions/index";
import RecipeCard from "./RecipeCard/RecipeCard";
import RefusedBadge from "../../UI/RefusedBadge/RefusedBadge";
import LoadingContainer from "../../UI/LoadingContainer/LoadingContainer";

const WaitingRecipeDetails = ({
  isAuthenticated,
  onSetAuthRedirectPath,
  authToken,
  match,
}) => {
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

  let redirect = null;
  if (!isAuthenticated) {
    redirect = <Redirect to={"/login"} />;
    onSetAuthRedirectPath("/waiting/" + match.params.id);
  }

  return (
    <React.Fragment>
      {redirect}
      <LoadingContainer isLoading={isLoading}>
        <RefusedBadge refused={data.pending_recipe.refused} />
        <RecipeCard recipe={data.pending_recipe} />
      </LoadingContainer>
    </React.Fragment>
  );
};

const mapStateToProps = (state) => {
  return {
    isAuthenticated: state.auth.access_token !== null,
    authToken: state.auth.access_token,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onSetAuthRedirectPath: (path) =>
      dispatch(actions.setAuthRedirectPath(path)),
  };
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(WaitingRecipeDetails);
