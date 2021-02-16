import React from "react";
import PropTypes from "prop-types";

import FullChefHat from "../Icons/FullChefHat";

const DifficultySymbol = ({ difficulty }) => {
  return (
    <span>
      {[...Array(difficulty)].map((e, i) => (
        <FullChefHat key={i} />
      ))}
    </span>
  );
};

DifficultySymbol.propTypes = {
  difficulty: PropTypes.number.isRequired,
};
export default DifficultySymbol;
