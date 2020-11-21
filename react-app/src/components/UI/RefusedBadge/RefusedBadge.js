import React from "react";
import { Badge } from "react-bootstrap";

const RefusedBadge = ({ refused }) => {
  const badge = refused ? (
    <Badge variant="danger">Odrzucony</Badge>
  ) : (
    <Badge variant="primary">Oczekujący</Badge>
  );

  return badge;
};

export default RefusedBadge;
