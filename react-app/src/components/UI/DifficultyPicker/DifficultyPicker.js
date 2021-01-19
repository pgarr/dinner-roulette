import React from "react";
import ReactStars from "react-rating-stars-component";
import EmptyChefHat from "../Icons/EmptyChefHat";
import FullChefHat from "../Icons/FullChefHat";

const DifficultyPicker = ({ onChange, disabled }) => {
  const iconSize = 2.5;

  return (
    <ReactStars
      count={3}
      onChange={onChange}
      isHalf={false}
      emptyIcon={<EmptyChefHat size={iconSize} />}
      filledIcon={<FullChefHat size={iconSize} />}
      edit={!disabled}
      a11y={false}
    />
  );
};

export default DifficultyPicker;
