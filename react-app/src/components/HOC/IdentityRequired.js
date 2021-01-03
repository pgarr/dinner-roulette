import React from "react";
import { withRouter } from "react-router-dom";
import { connect } from "react-redux";
import { toast } from "react-toastify";

import { getIdentity } from "../../shared/tokenDecode";

const IdentityRequired = ({
  children,
  identity,
  history,
  requiredIdentity,
}) => {
  if (requiredIdentity && identity !== requiredIdentity) {
    toast.error("Nie masz uprawnień do tej akcji");
    history.goBack();
  }

  return <React.Fragment>{children}</React.Fragment>;
};

const mapStateToProps = (state) => {
  return {
    identity: getIdentity(state.auth.access_token),
  };
};

export default withRouter(connect(mapStateToProps)(IdentityRequired));
