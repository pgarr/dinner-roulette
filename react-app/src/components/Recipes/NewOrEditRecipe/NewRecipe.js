import React, { useReducer, useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { toast } from "react-toastify";

import AuthRequired from "../../HOC/AuthRequired";
import RecipeForm from "./RecipeForm/RecipeForm";
import axios from "../../../shared/axios-api";
import { axiosError } from "../../../shared/errors";
import recipeReducer from "../utils/recipeReducer";
import { newRecipe } from "../utils/baseRecipeObjects";

const NewRecipe = ({ authToken }) => {
  const [recipe, dispatchRecipe] = useReducer(recipeReducer, newRecipe());
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(false);

  const submitHandler = async (event) => {
    event.preventDefault();

    setLoading(true);
    try {
      const response = await axios.post("/recipes", recipe, {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
      dispatchRecipe({
        type: "CHANGE",
        data: { id: response.data.pending_recipe.id },
      });
      toast.info(
        "Przepis będzie widoczny dla innych użytkowników po zatwierdzeniu przez administratora."
      );
      setSaved(true);
    } catch (error) {
      axiosError(error);
      setLoading(false);
    }
  };

  if (saved && recipe.id) {
    return <Redirect to={"/pendingrecipes/" + recipe.id} />;
  }

  return (
    <AuthRequired>
      <h1>Utwórz nowy przepis</h1>
      <RecipeForm
        recipe={recipe}
        loading={loading}
        onSubmit={submitHandler}
        dispatchRecipe={dispatchRecipe}
      ></RecipeForm>
    </AuthRequired>
  );
};

const mapStateToProps = (state) => {
  return {
    authToken: state.auth.access_token,
  };
};

export default connect(mapStateToProps)(NewRecipe);
