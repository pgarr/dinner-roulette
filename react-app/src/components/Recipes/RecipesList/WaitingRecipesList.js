import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";

import useFetchApi from "../../../shared/customHooks/useFetchApi";
import * as actions from "../../../store/actions/index";
import NumberedPagination from "../../UI/NumberedPagination/NumberedPagination";
import RecipesTable from "./RecipesTable/RecipesTable";

const WaitingRecipesList = ({
  isAuthenticated,
  onSetAuthRedirectPath,
  authToken,
  history,
}) => {
  const [{ data, isLoading, isError }, doFetch] = useFetchApi(
    {
      url: "/waiting",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    },
    {
      pending_recipes: [],
      _meta: { page: 1, total_pages: 1 },
    },
    isAuthenticated
  );

  const recipeSelectedHandler = (id) => {
    history.push({ pathname: "/pendingrecipes/" + id });
  };

  const pageChangedHandler = (page) => {
    doFetch({
      url: `/waiting?page=${page}`,
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });
  };

  let redirect = null;
  if (!isAuthenticated) {
    redirect = <Redirect to={"/login"} />;
    onSetAuthRedirectPath("/pendingrecipes");
  }

  return (
    <React.Fragment>
      {redirect}
      <RecipesTable
        recipes={data.pending_recipes}
        onSelectRecipe={recipeSelectedHandler}
        showPendingStatus={true}
      />
      <NumberedPagination
        activePage={data._meta.page}
        totalPages={data._meta.total_pages}
        onChangePage={pageChangedHandler}
      />
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

export default connect(mapStateToProps, mapDispatchToProps)(WaitingRecipesList);
