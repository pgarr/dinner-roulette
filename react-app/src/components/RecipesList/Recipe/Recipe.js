import React from "react";

import DifficultySymbol from "../../DifficultySymbol/DifficultySymbol";

const Recipe = (props) => (
  <tr>
    <th scope="row">{props.index}</th>
    <td>{props.title}</td>
    <td>{props.time}'</td>
    <td>
      <DifficultySymbol difficulty={props.difficulty} />
    </td>
  </tr>
);

export default Recipe;
