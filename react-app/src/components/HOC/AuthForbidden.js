import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";

const AuthForbidden = ({ children, isAuthenticated, authRedirectPath }) => {
  if (isAuthenticated) {
    return <Redirect to={authRedirectPath} />;
  }

  return <React.Fragment>{children}</React.Fragment>;
};

const mapStateToProps = (state) => {
  return {
    isAuthenticated: state.auth.access_token !== null,
    authRedirectPath: state.auth.authRedirectPath,
  };
};

export default connect(mapStateToProps)(AuthForbidden);
