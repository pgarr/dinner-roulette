import React, { useEffect, useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";

import axios from "../../../shared/axios-api";
import * as actions from "../../../store/actions/index";
import NumberedPagination from "../../UI/NumberedPagination/NumberedPagination";
import RecipesTable from "./RecipesTable/RecipesTable";

const MyRecipesList = ({
  isAuthenticated,
  onSetAuthRedirectPath,
  authToken,
  history,
}) => {
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
        const response = await axios.get("/recipes/my?page=" + activePage, {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });
        setRecipes(response.data.recipes);
        setTotalPages(response.data._meta.total_pages);
      } catch (error) {
        console.log(error);
        setIsError(true);
      }
      setIsLoading(false);
    };

    if (isAuthenticated) {
      fetchData();
    }
  }, [activePage, authToken, isAuthenticated]);

  const recipeSelectedHandler = (id) => {
    history.push({ pathname: "/recipes/" + id });
  };

  const pageChangedHandler = (page) => {
    setActivePage(page);
  };

  let redirect = null;
  if (!isAuthenticated) {
    redirect = <Redirect to={"/login"} />;
    onSetAuthRedirectPath("/myrecipes");
  }

  return (
    <React.Fragment>
      {redirect}
      <RecipesTable recipes={recipes} onSelectRecipe={recipeSelectedHandler} />
      <NumberedPagination
        activePage={activePage}
        totalPages={totalPages}
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

export default connect(mapStateToProps, mapDispatchToProps)(MyRecipesList);
