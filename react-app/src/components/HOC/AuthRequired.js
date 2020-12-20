import React from "react";
import { connect } from "react-redux";
import { withRouter, Redirect } from "react-router-dom";

import * as actions from "../../store/actions/index";

const AuthRequired = ({
  children,
  isAuthenticated,
  onSetAuthRedirectPath,
  location,
}) => {
  if (!isAuthenticated) {
    onSetAuthRedirectPath(location.pathname);
    return <Redirect to={"/login"} />;
  }

  return <React.Fragment>{children}</React.Fragment>;
};

const mapStateToProps = (state) => {
  return {
    isAuthenticated: state.auth.access_token !== null,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onSetAuthRedirectPath: (path) =>
      dispatch(actions.setAuthRedirectPath(path)),
  };
};

export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(AuthRequired)
);
