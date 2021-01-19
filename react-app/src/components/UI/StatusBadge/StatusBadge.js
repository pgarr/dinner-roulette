import React from "react";
import { Badge } from "react-bootstrap";

const StatusBadge = ({ status }) => {
  switch (status) {
    case "refused":
      return <Badge variant="danger">Odrzucony</Badge>;
    case "pending":
      return <Badge variant="primary">Oczekujący</Badge>;
    case "accepted":
      return <Badge variant="success">Aktywny</Badge>;
    default:
      return null;
  }
};

export default StatusBadge;
