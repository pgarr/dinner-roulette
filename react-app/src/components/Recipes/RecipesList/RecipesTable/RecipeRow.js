import React from "react";

import DifficultySymbol from "../../../UI/DifficultySymbol/DifficultySymbol";
import RefusedBadge from "../../../UI/RefusedBadge/RefusedBadge";

const Recipe = ({ index, title, time, difficulty, clicked, refused }) => {
  return (
    <tr onClick={clicked}>
      <th scope="row">{index}</th>
      <td>{title}</td>
      <td>{time ? time + "'" : null}</td>
      <td>
        {difficulty ? <DifficultySymbol difficulty={difficulty} /> : null}
      </td>
      {refused !== null && (
        <td>
          <RefusedBadge refused={refused} />
        </td>
      )}
    </tr>
  );
};

export default Recipe;
