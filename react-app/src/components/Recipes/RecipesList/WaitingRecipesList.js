import React from "react";
import { connect } from "react-redux";

import useFetchApi from "../../../shared/customHooks/useFetchApi";
import LoadingContainer from "../../UI/LoadingContainer/LoadingContainer";
import NumberedPagination from "../../UI/NumberedPagination/NumberedPagination";
import RecipesTable from "./RecipesTable/RecipesTable";

const WaitingRecipesList = ({ isAuthenticated, authToken, history }) => {
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
      url: "/waiting",
      params: { page },
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });
  };

  return (
    <React.Fragment>
      <LoadingContainer isLoading={isLoading}>
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

export default connect(mapStateToProps)(WaitingRecipesList);
