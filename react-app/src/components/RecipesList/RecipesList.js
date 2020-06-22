import React, { useEffect } from "react";
import { connect } from "react-redux";
import { Table, Pagination } from "react-bootstrap";
import PropTypes from "prop-types";

import Recipe from "./Recipe/Recipe";
import * as actions from "../../store/actions/index";

const RecipesList = ({
  recipes,
  onFetchRecipes,
  activePage,
  totalPages,
  onChangePage,
  history,
}) => {
  useEffect(() => {
    onFetchRecipes(activePage);
  }, [onFetchRecipes, activePage]);

  const recipeSelectedHandler = (id) => {
    history.push({ pathname: "/recipes/" + id });
  };

  // Pagination
  let items = [];
  for (let number = 1; number <= totalPages; number++) {
    items.push(
      <Pagination.Item
        key={number}
        active={number === activePage}
        onClick={
          number === activePage
            ? null
            : (event) => onChangePage(event.target.text)
        }
      >
        {number}
      </Pagination.Item>
    );
  }

  return (
    <React.Fragment>
      <Table hover>
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Nazwa</th>
            <th scope="col">Czas</th>
            <th scope="col">Trudność</th>
          </tr>
        </thead>
        <tbody>
          {recipes.map((recipe, index) => {
            return (
              <Recipe
                index={index + 1}
                {...recipe}
                key={recipe.id}
                clicked={() => recipeSelectedHandler(recipe.id)}
              />
            );
          })}
        </tbody>
      </Table>
      <Pagination size="sm">{items}</Pagination>
    </React.Fragment>
  );
};

const mapStateToProps = (state) => {
  return {
    loading: state.recipes.loading,
    recipes: state.recipes.recipes,
    activePage: state.recipes.activePage,
    totalPages: state.recipes.totalPages,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onFetchRecipes: (page) => dispatch(actions.fetchRecipes(page)),
    onChangePage: (page) => dispatch(actions.changePage(page)),
  };
};

RecipesList.propTypes = {
  recipes: PropTypes.array.isRequired,
};

export default connect(mapStateToProps, mapDispatchToProps)(RecipesList);
