import React from "react";

import DifficultySymbol from "../../../UI/DifficultySymbol/DifficultySymbol";
import StatusBadge from "../../../UI/StatusBadge/StatusBadge";

const RecipeRow = ({ index, title, time, difficulty, clicked, status }) => {
  return (
    <tr onClick={clicked}>
      <th scope="row">{index}</th>
      <td>{title}</td>
      <td>{time ? time + "'" : null}</td>
      <td>
        {difficulty ? <DifficultySymbol difficulty={difficulty} /> : null}
      </td>
      {status !== null && (
        <td>
          <StatusBadge status={status} />
        </td>
      )}
    </tr>
  );
};

export default RecipeRow;
