import React from "react";
import ReactStars from "react-rating-stars-component";
import EmptyChefHat from "../Icons/EmptyChefHat";
import FullChefHat from "../Icons/FullChefHat";

const DifficultyPicker = ({ onChange, disabled, initialValue }) => {
  const iconSize = 2.5;
  //TODO: value dont update when props changes - ReactStars bug
  // find better library, implement own solution, fix bug in library
  return (
    <ReactStars
      count={3}
      onChange={onChange}
      isHalf={false}
      emptyIcon={<EmptyChefHat size={iconSize} />}
      filledIcon={<FullChefHat size={iconSize} />}
      edit={!disabled}
      a11y={false}
      value={initialValue}
    />
  );
};

export default DifficultyPicker;
