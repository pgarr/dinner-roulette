import React from "react";

import { ReactComponent as FullHatImage } from "../../../svg/chef-hat-svgrepo-color.svg";

const FullChefHat = ({ size }) => {
  size = size || 1.5;
  const style = { height: size + "rem" };

  return <FullHatImage style={style} />;
};

export default FullChefHat;
