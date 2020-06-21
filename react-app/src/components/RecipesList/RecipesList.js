import React, { useEffect } from "react";
import { connect } from "react-redux";
import { Table } from "react-bootstrap";
import PropTypes from "prop-types";

import Recipe from "./Recipe/Recipe";
import * as actions from "../../store/actions/index";

const RecipesList = ({ recipes, onFetchRecipes }) => {
  useEffect(() => {
    onFetchRecipes();
  }, [onFetchRecipes]);

  return (
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
          return <Recipe index={index} {...recipe} key={recipe.id} />;
        })}
      </tbody>
    </Table>
  );
};

const mapStateToProps = (state) => {
  return {
    recipes: state.recipe.recipes,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onFetchRecipes: () => dispatch(actions.fetchRecipes()),
  };
};

RecipesList.propTypes = {
  recipes: PropTypes.array.isRequired,
};

export default connect(mapStateToProps, mapDispatchToProps)(RecipesList);
