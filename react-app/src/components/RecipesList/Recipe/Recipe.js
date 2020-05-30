import React from "react";

const Recipe = (props) => (
  <tr>
    <th scope="row">{props.index}</th>
    <td>{props.title}</td>
    <td>{props.time}'</td>
    <td>{props.difficulty}</td>
  </tr>
);

export default Recipe;
