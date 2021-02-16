import React from "react";

import { ReactComponent as EmptyHatImage } from "../../../svg/chef-hat-chef-svgrepo-gray.svg";

const EmptyChefHat = ({ size }) => {
  size = size || 1.5;
  const style = { fill: "#f2f2f2", height: size + "rem" };

  return <EmptyHatImage style={style} />;
};

export default EmptyChefHat;
