import React from "react";
import { connect } from "react-redux";

import useFetchApi from "../../../shared/customHooks/useFetchApi";
import AuthRequired from "../../HOC/AuthRequired";
import LoadingContainer from "../../HOC/LoadingContainer/LoadingContainer";
import NumberedPagination from "../../UI/NumberedPagination/NumberedPagination";
import RecipesTable from "./RecipesTable/RecipesTable";

const MyRecipesList = ({ isAuthenticated, authToken, history }) => {
  const [{ data, isLoading }, doFetch] = useFetchApi(
    {
      url: "/recipes/my",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    },
    {
      recipes: [],
      _meta: { page: 1, total_pages: 1 },
    },
    isAuthenticated
  );

  const recipeSelectedHandler = (id) => {
    history.push({ pathname: "/myrecipes/" + id });
  };

  const pageChangedHandler = (page) => {
    doFetch({
      url: `/recipes/my`,
      params: { page },
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });
  };

  return (
    <AuthRequired>
      <LoadingContainer isLoading={isLoading}>
        <RecipesTable
          recipes={data.recipes}
          onSelectRecipe={recipeSelectedHandler}
          showStatus
        />
        <NumberedPagination
          activePage={data._meta.page}
          totalPages={data._meta.total_pages}
          onChangePage={pageChangedHandler}
        />
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

export default connect(mapStateToProps)(MyRecipesList);
