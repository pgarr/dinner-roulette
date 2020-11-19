import React, { useEffect, Suspense } from "react";
import { Route, Switch, withRouter, Redirect } from "react-router-dom";
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
import RecipesList from "../Recipes/RecipesList/RecipesList";
import MyRecipesList from "../Recipes/RecipesList/MyRecipesList";
import WaitingRecipesList from "../Recipes/RecipesList/WaitingRecipesList";
import RecipeCard from "../Recipes/RecipeCard/RecipeCard";
import Home from "../Home/Home";
import Auth from "../Auth/Auth";
import * as actions from "../../store/actions/index";
import Logout from "../Auth/Logout/Logout";
import Register from "../Auth/Register/Register";
import RecipeForm from "../RecipeForm/RecipeForm";

const App = ({ onTryAutoSingup }) => {
  library.add(faClock, faPlus, farFaStar, fasFaStar, faUser);

  useEffect(() => {
    onTryAutoSingup();
  }, [onTryAutoSingup]);

  let routes = (
    <Switch>
      <Route path="/recipes" exact component={RecipesList} />
      <Route path="/myrecipes" component={MyRecipesList} />
      <Route path="/pendingrecipes" component={WaitingRecipesList} />
      <Route path="/recipes/:id" component={RecipeCard} />
      <Route path="/login" component={Auth} />
      <Route path="/logout" component={Logout} />
      <Route path="/register" component={Register} />
      <Route path="/newrecipe" component={RecipeForm} />
      <Route path="/" exact component={Home} />
      <Redirect to="/" />
    </Switch>
  );

  return (
    <div>
      <Layout>
        <Suspense fallback={<p>Loading...</p>}>{routes}</Suspense>
      </Layout>
    </div>
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
