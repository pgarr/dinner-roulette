import React from "react";

const Ingredient = (props) => {
  return (
    <tr>
      <td>{props.name}</td>
      <td>{`${props.amount} ${props.unit}`}</td>
    </tr>
  );
};

export default Ingredient;
