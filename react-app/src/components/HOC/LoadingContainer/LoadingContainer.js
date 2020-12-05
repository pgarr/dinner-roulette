import React from "react";
import { Spinner } from "react-bootstrap";

import styles from "./LoadingContainer.module.css";

const LoadingContainer = ({ isLoading, children }) => {
  const display = isLoading ? (
    <div className={styles.Center}>
      <Spinner animation="border" role="status">
        <span className="sr-only">Loading...</span>
      </Spinner>
    </div>
  ) : (
    children
  );

  return display;
};

export default LoadingContainer;
