import React from "react";
import { Table } from "react-bootstrap";
import PropTypes from "prop-types";

import Ingredient from "./Ingredient/Ingredient";

const IngredientList = (props) => {
  return (
    <Table hover>
      <thead>
        <tr>
          <th scope="col">Nazwa</th>
          <th scope="col">Ilość</th>
        </tr>
      </thead>
      <tbody>
        {props.ingredients.map((ingredient, index) => {
          return <Ingredient key={index} {...ingredient} />;
        })}
      </tbody>
    </Table>
  );
};

IngredientList.propTypes = {
  ingredients: PropTypes.array.isRequired,
};

export default IngredientList;
