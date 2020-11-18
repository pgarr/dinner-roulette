import React from "react";

import useFetchApi from "../../../shared/customHooks/useFetchApi";
import NumberedPagination from "../../UI/NumberedPagination/NumberedPagination";
import RecipesTable from "./RecipesTable/RecipesTable";

const RecipesList = ({ history }) => {
  const [{ data, isLoading, isError }, doFetch] = useFetchApi("/recipes", {
    recipes: [],
    _meta: { page: 1, total_pages: 1 },
  });

  const recipeSelectedHandler = (id) => {
    history.push({ pathname: "/recipes/" + id });
  };

  const pageChangedHandler = (page) => {
    doFetch(`/recipes?page=${page}`);
  };

  return (
    <React.Fragment>
      <RecipesTable
        recipes={data.recipes}
        onSelectRecipe={recipeSelectedHandler}
      />
      <NumberedPagination
        activePage={data._meta.page}
        totalPages={data._meta.total_pages}
        onChangePage={pageChangedHandler}
      />
    </React.Fragment>
  );
};

export default RecipesList;
