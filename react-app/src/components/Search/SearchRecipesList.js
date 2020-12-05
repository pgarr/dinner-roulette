import React, { useEffect } from "react";
import { connect } from "react-redux";

import * as actions from "../../store/actions/index";
import useFetchApi from "../../shared/customHooks/useFetchApi";
import LoadingContainer from "../HOC/LoadingContainer/LoadingContainer";
import NumberedPagination from "../UI/NumberedPagination/NumberedPagination";
import RecipesTable from "../Recipes/RecipesList/RecipesTable/RecipesTable";
import SearchBadges from "./SearchBadges/SearchBadges";

const SearchRecipesList = ({ history, q, onSetSearchFunction }) => {
  const [{ data, isLoading, isError }, doFetch] = useFetchApi(
    { url: "/search", params: { q } },
    {
      recipes: [],
      _meta: { page: 1, total_pages: 1 },
    },
    q !== ""
  );

  useEffect(() => {
    const search = (text) => {
      doFetch({ url: "/search", params: { q: text } });
    };
    onSetSearchFunction(search);
  }, [onSetSearchFunction, doFetch]);

  const recipeSelectedHandler = (id) => {
    history.push({ pathname: "/recipes/" + id });
  };

  const pageChangedHandler = (page) => {
    doFetch({ url: "/search", params: { q, page } });
  };

  return (
    <LoadingContainer isLoading={isLoading}>
      <SearchBadges />
      <RecipesTable
        recipes={data.recipes}
        onSelectRecipe={recipeSelectedHandler}
      />
      <NumberedPagination
        activePage={data._meta.page}
        totalPages={data._meta.total_pages}
        onChangePage={pageChangedHandler}
      />
    </LoadingContainer>
  );
};

const mapStateToProps = (state) => {
  return {
    q: state.search.q,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onSetSearchFunction: (func) => dispatch(actions.setSearchFunction(func)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(SearchRecipesList);
