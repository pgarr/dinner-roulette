import React from "react";
import { withRouter } from "react-router-dom";
import { connect } from "react-redux";
import { Button, Form, FormControl } from "react-bootstrap";

import * as actions from "../../store/actions/index";

const SearchWidget = ({
  q,
  onSetSearchQ,
  history,
  location,
  doSearch,
  onSetSearchBadges,
}) => {
  const submitHandler = (event) => {
    event.preventDefault();
    onSetSearchBadges();
    const searchPath = "/search";
    if (location.pathname === searchPath) {
      doSearch(q);
    } else {
      history.push({ pathname: "/search" });
    }
    onSetSearchBadges();
  };

  return (
    <Form inline onSubmit={submitHandler}>
      <FormControl
        type="text"
        required
        placeholder="Szukaj"
        className="mr-sm-2"
        value={q}
        onChange={(event) => onSetSearchQ(event.target.value)}
      />
      <Button variant="outline-info" type="submit">
        Szukaj
      </Button>
    </Form>
  );
};

const mapStateToProps = (state) => {
  return {
    q: state.search.q,
    doSearch: state.search.func,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onSetSearchQ: (q) => dispatch(actions.setSearchQ(q)),
    onSetSearchBadges: () => dispatch(actions.setSearchBadges()),
  };
};

export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(SearchWidget)
);
