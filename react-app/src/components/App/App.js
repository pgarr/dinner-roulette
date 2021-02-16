import React, { useEffect } from "react";
import { withRouter } from "react-router-dom";
import { connect } from "react-redux";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faClock,
  faPlus,
  faStar as fasFaStar,
  faUser,
} from "@fortawesome/free-solid-svg-icons";
import { faStar as farFaStar } from "@fortawesome/free-regular-svg-icons";

import Layout from "../Layout/Layout";
import * as actions from "../../store/actions/index";
import RoutesList from "./RoutesList";

const App = ({ onTryAutoSingup }) => {
  // awesome icons library
  library.add(faClock, faPlus, farFaStar, fasFaStar, faUser);

  useEffect(() => {
    onTryAutoSingup();
  }, [onTryAutoSingup]);

  return (
    <Layout>
      <RoutesList />
    </Layout>
  );
};

const mapStateToProps = (state) => {
  return {};
};

const mapDispatchToProps = (dispatch) => {
  return {
    onTryAutoSingup: () => dispatch(actions.authCheckState()),
  };
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(App));
