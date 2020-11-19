import React from "react";
import { Badge } from "react-bootstrap";

import DifficultySymbol from "../../../UI/DifficultySymbol/DifficultySymbol";

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
          {refused ? (
            <Badge variant="danger">Odrzucony</Badge>
          ) : (
            <Badge variant="primary">Oczekujący</Badge>
          )}
        </td>
      )}
    </tr>
  );
};

export default Recipe;
