import React, { useEffect, useState } from "react";

import axios from "../../../shared/axios-api";
import NumberedPagination from "../../UI/NumberedPagination/NumberedPagination";
import RecipesTable from "./RecipesTable/RecipesTable";

const RecipesList = ({ history }) => {
  const [activePage, setActivePage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [recipes, setRecipes] = useState([]);

  const [isLoading, setIsLoading] = useState(false); //TODO
  const [isError, setIsError] = useState(false); //TODO

  useEffect(() => {
    const fetchData = async () => {
      setIsError(false);
      setIsLoading(true);

      try {
        const response = await axios.get("/recipes?page=" + activePage);
        setRecipes(response.data.recipes);
        setTotalPages(response.data._meta.total_pages);
      } catch (error) {
        console.log(error);
        setIsError(true);
      }
      setIsLoading(false);
    };

    fetchData();
  }, [activePage]);

  const recipeSelectedHandler = (id) => {
    history.push({ pathname: "/recipes/" + id });
  };

  const pageChangedHandler = (page) => {
    setActivePage(page);
  };

  return (
    <React.Fragment>
      <RecipesTable recipes={recipes} onSelectRecipe={recipeSelectedHandler} />
      <NumberedPagination
        activePage={activePage}
        totalPages={totalPages}
        onChangePage={pageChangedHandler}
      />
    </React.Fragment>
  );
};

export default RecipesList;
