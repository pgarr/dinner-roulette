import React from "react";
import { Table } from "react-bootstrap";

import Recipe from "./RecipeRow";

const RecipesTable = ({ recipes, onSelectRecipe, isPending }) => {
  return (
    <Table hover>
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Nazwa</th>
          <th scope="col">Czas</th>
          <th scope="col">Trudność</th>
          {isPending && <th scope="col">Status</th>}
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
              refused={isPending ? recipe.refused : null}
            />
          );
        })}
      </tbody>
    </Table>
  );
};

export default RecipesTable;
