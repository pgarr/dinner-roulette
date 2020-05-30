import React from "react";
import { Table } from "react-bootstrap";
import PropTypes from "prop-types";

import Recipe from "./Recipe/Recipe";

const RecipesList = (props) => {
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
        {props.recipes.map((recipe, index) => {
          return <Recipe index={index} {...recipe} key={recipe.id} />;
        })}
      </tbody>
    </Table>
  );
};

RecipesList.propTypes = {
  recipes: PropTypes.array.isRequired,
};

export default RecipesList;
