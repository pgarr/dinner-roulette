import React from "react";
import { Table } from "react-bootstrap";

import RecipeRow from "./RecipeRow";

const RecipesTable = ({ recipes, onSelectRecipe, showStatus }) => {
  return (
    <Table hover>
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Nazwa</th>
          <th scope="col">Czas</th>
          <th scope="col">Trudność</th>
          {showStatus && <th scope="col">Status</th>}
        </tr>
      </thead>
      <tbody>
        {recipes.map((recipe, index) => {
          return (
            <RecipeRow
              index={index + 1}
              {...recipe}
              key={recipe.id}
              clicked={() => onSelectRecipe(recipe.id)}
              status={showStatus ? recipe.status : null}
            />
          );
        })}
      </tbody>
    </Table>
  );
};

export default RecipesTable;
