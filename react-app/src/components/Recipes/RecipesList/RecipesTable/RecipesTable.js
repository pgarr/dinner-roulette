import React from "react";
import { Table } from "react-bootstrap";

import Recipe from "./RecipeRow";

const RecipesTable = ({ recipes, onSelectRecipe }) => {
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
          return (
            <Recipe
              index={index + 1}
              {...recipe}
              key={recipe.id}
              clicked={() => onSelectRecipe(recipe.id)}
            />
          );
        })}
      </tbody>
    </Table>
  );
};

export default RecipesTable;
