import React from "react";

const Ingredient = ({ title, amount, unit }) => {
  return (
    <tr>
      <td>{title}</td>
      {amount && <td>{`${amount} ${unit}`}</td>}
    </tr>
  );
};

export default Ingredient;
