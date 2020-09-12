import React from "react";
import { Route, Switch } from "react-router-dom";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faClock,
  faPlus,
  faStar as fasFaStar,
  faUser,
} from "@fortawesome/free-solid-svg-icons";
import { faStar as farFaStar } from "@fortawesome/free-regular-svg-icons";

import Layout from "../Layout/Layout";
import RecipesList from "../RecipesList/RecipesList";
import RecipeCard from "../RecipeCard/RecipeCard";
import Home from "../Home/Home";
import Auth from "../Auth/Auth";

const App = (props) => {
  library.add(faClock, faPlus, farFaStar, fasFaStar, faUser);

  return (
    <div>
      <Layout>
        <Switch>
          <Route path="/recipes" exact component={RecipesList} />
          <Route path="/recipes/:id" component={RecipeCard} />
          <Route path="/login" component={Auth} />
          <Route path="/" exact component={Home} />
        </Switch>
      </Layout>
    </div>
  );
};

export default App;
