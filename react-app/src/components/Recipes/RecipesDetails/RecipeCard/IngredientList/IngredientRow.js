import React from "react";

const IngredientRow = ({ title, amount, unit }) => {
  return (
    <tr>
      <td>{title}</td>
      <td>{amount ? `${amount} ${unit}` : unit}</td>
    </tr>
  );
};

export default IngredientRow;
