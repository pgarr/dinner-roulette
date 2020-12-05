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
  let redirect = null;
  if (!isAuthenticated) {
    redirect = <Redirect to={"/login"} />;
    console.log(location.pathname);
    onSetAuthRedirectPath(location.pathname);
  }

  return (
    <React.Fragment>
      {redirect}
      {children}
    </React.Fragment>
  );
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
