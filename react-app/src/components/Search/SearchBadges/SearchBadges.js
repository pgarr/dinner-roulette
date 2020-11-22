import React from "react";
import { connect } from "react-redux";
import { Badge } from "react-bootstrap";

import styles from "./SearchBadges.module.css";

const SearchBadges = ({ badges }) => {
  return badges.map((badge, index) => {
    return (
      <Badge variant="info" key={index} className={styles.Badge}>
        {badge}
      </Badge>
    );
  });
};

const mapStateToProps = (state) => {
  return {
    q: state.search.q,
    badges: state.search.badges,
  };
};

export default connect(mapStateToProps)(SearchBadges);
