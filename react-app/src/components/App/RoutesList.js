import React from "react";
import { Route, Switch, Redirect } from "react-router-dom";

import RecipesList from "../Recipes/RecipesList/RecipesList";
import MyRecipesList from "../Recipes/RecipesList/MyRecipesList";
import WaitingRecipesList from "../Recipes/RecipesList/WaitingRecipesList";
import SearchRecipesList from "../Search/SearchRecipesList";
import Home from "../Home/Home";
import Auth from "../Auth/Auth";
import Logout from "../Auth/Logout/Logout";
import Register from "../Auth/Register/Register";
import RecipeDetails from "../Recipes/RecipesDetails/RecipeDetails";
import WaitingRecipeDetails from "../Recipes/RecipesDetails/WaitingRecipeDetails";
import ResetPassword from "../Auth/ResetPassword/ResetPassword";
import SetPassword from "../Auth/ResetPassword/SetPassword";
import NewRecipe from "../Recipes/NewOrEditRecipe/NewRecipe";
import EditWaitingRecipe from "../Recipes/NewOrEditRecipe/EditWaitingRecipe";

const RoutesList = () => {
  return (
    <Switch>
      <Route path="/recipes" exact component={RecipesList} />
      <Route path="/myrecipes" exact component={MyRecipesList} />
      <Route path="/pendingrecipes" exact component={WaitingRecipesList} />
      <Route path="/recipes/:id" component={RecipeDetails} />
      <Route
        path="/pendingrecipes/:id"
        exact
        component={WaitingRecipeDetails}
      />
      <Route
        path="/pendingrecipes/:id/edit"
        exact
        component={EditWaitingRecipe}
      />
      <Route path="/search" component={SearchRecipesList} />
      <Route path="/login" component={Auth} />
      <Route path="/logout" component={Logout} />
      <Route path="/register" component={Register} />
      <Route path="/resetrequest" component={ResetPassword} />
      <Route path="/reset_password/:token" component={SetPassword} />
      <Route path="/newrecipe" component={NewRecipe} />
      <Route path="/" exact component={Home} />
      <Redirect to="/" />
    </Switch>
  );
};

export default RoutesList;
