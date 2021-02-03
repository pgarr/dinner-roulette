import React from "react";
import { Route, Switch, Redirect } from "react-router-dom";

import RecipesList from "../Recipes/RecipesList/RecipesList";
import MyRecipesList from "../Recipes/RecipesList/MyRecipesList";
import Home from "../Home/Home";
import Auth from "../Auth/Auth";
import Logout from "../Auth/Logout/Logout";
import Register from "../Auth/Register/Register";
import RecipeDetails from "../Recipes/RecipesDetails/RecipeDetails";
import MyRecipeDetails from "../Recipes/RecipesDetails/MyRecipeDetails";
import ResetPassword from "../Auth/ResetPassword/ResetPassword";
import SetPassword from "../Auth/ResetPassword/SetPassword";
import NewRecipe from "../Recipes/NewOrEditRecipe/NewRecipe";
import EditRecipe from "../Recipes/NewOrEditRecipe/EditRecipe";

const RoutesList = () => {
  return (
    <Switch>
      <Route path="/recipes" exact component={RecipesList} />
      <Route path="/recipes/:id" component={RecipeDetails} />
      <Route path="/myrecipes" exact component={MyRecipesList} />
      <Route path="/myrecipes/:id" component={MyRecipeDetails} />
      <Route path="/login" component={Auth} />
      <Route path="/logout" component={Logout} />
      <Route path="/register" component={Register} />
      <Route path="/resetrequest" component={ResetPassword} />
      <Route path="/reset_password/:token" component={SetPassword} />
      <Route path="/newrecipe" component={NewRecipe} />
      <Route path="/editrecipe/:id" component={EditRecipe} />
      <Route path="/" exact component={Home} />
      <Redirect to="/" />
    </Switch>
  );
};

export default RoutesList;
