import React from "react";

import DifficultySymbol from "../../../UI/DifficultySymbol/DifficultySymbol";

const Recipe = ({ index, title, time, difficulty, clicked }) => {
  return (
    <tr onClick={clicked}>
      <th scope="row">{index}</th>
      <td>{title}</td>
      <td>{time ? time + "'" : null}</td>
      <td>
        {difficulty ? <DifficultySymbol difficulty={difficulty} /> : null}
      </td>
    </tr>
  );
};

export default Recipe;
