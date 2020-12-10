import React from "react";

import useFetchApi from "../../../shared/customHooks/useFetchApi";
import LoadingContainer from "../../HOC/LoadingContainer/LoadingContainer";
import NumberedPagination from "../../UI/NumberedPagination/NumberedPagination";
import RecipesTable from "./RecipesTable/RecipesTable";

const RecipesList = ({ history }) => {
  const [{ data, isLoading }, doFetch] = useFetchApi(
    { url: "/recipes" },
    {
      recipes: [],
      _meta: { page: 1, total_pages: 1 },
    }
  );

  const recipeSelectedHandler = (id) => {
    history.push({ pathname: "/recipes/" + id });
  };

  const pageChangedHandler = (page) => {
    doFetch({ url: "/recipes", params: { page } });
  };

  return (
    <LoadingContainer isLoading={isLoading}>
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

export default RecipesList;
