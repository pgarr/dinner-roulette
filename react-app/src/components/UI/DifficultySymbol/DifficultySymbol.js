import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import PropTypes from "prop-types";

const DifficultySymbol = (props) => {
  const max = 5;
  return (
    props.difficulty <= max && (
      <span>
        {[...Array(props.difficulty)].map((e, i) => (
          <FontAwesomeIcon key={i} icon="star" />
        ))}
        {[...Array(max - props.difficulty)].map((e, i) => (
          <FontAwesomeIcon key={i} icon={["far", "star"]} />
        ))}
      </span>
    )
  );
};

DifficultySymbol.propTypes = {
  difficulty: PropTypes.number.isRequired,
};
export default DifficultySymbol;

// {% for i in range(recipe.difficulty) %}
//     <i class="fas fa-star"></i>
// {% endfor %}
// {% for i in range(5-recipe.difficulty) %}
//     <i class="far fa-star"></i>
// {% endfor %}
// [...Array(n)].map((e, i) => <span className="busterCards" key={i}>♦</span>)
