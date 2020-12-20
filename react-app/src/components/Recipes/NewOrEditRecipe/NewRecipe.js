import React, { useReducer, useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { v4 as uuidv4 } from "uuid";
import { toast } from "react-toastify";

import AuthRequired from "../../HOC/AuthRequired";
import RecipeForm from "./RecipeForm/RecipeForm";
import axios from "../../../shared/axios-api";
import { axiosError } from "../../../shared/errors";

const newIngredient = () => ({ id: uuidv4(), title: "", amount: "", unit: "" });

const newRecipe = {
  title: "",
  time: 0,
  difficulty: 0,
  ingredients: [],
  link: "",
  preparation: "",
  id: null,
};

const recipeReducer = (state, action) => {
  switch (action.type) {
    case "CHANGE":
      return { ...state, ...action.data };
    case "ADD_INGREDIENT":
      const addedIngredients = state.ingredients.concat(newIngredient());
      return { ...state, ingredients: addedIngredients };
    case "REMOVE_INGREDIENT":
      const removedIngredients = state.ingredients.filter(
        (ingredient) => ingredient.id !== action.id
      );
      return { ...state, ingredients: removedIngredients };
    case "CHANGE_INGREDIENT":
      const mappedIngredients = state.ingredients.map((ingredient) => {
        if (ingredient.id === action.id) {
          const updatedIngredient = { ...ingredient, ...action.changes };
          return updatedIngredient;
        }
        return ingredient;
      });
      return { ...state, ingredients: mappedIngredients };
    default:
      return state;
  }
};

const NewRecipe = ({ authToken }) => {
  const [recipe, dispatchRecipe] = useReducer(recipeReducer, newRecipe);
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(false);

  const submitHandler = async (event) => {
    event.preventDefault();

    setLoading(true);
    try {
      const response = await axios.post("/recipe", recipe, {
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
