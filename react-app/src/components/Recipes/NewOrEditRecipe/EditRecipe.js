import React, { useEffect, useReducer, useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { toast } from "react-toastify";

import AuthRequired from "../../HOC/AuthRequired";
import RecipeForm from "./RecipeForm/RecipeForm";
import axios from "../../../shared/axios-api";
import { axiosError } from "../../../shared/errors";
import recipeReducer from "../utils/recipeReducer";
import { newRecipe } from "../utils/baseRecipeObjects";
import { getIdentity } from "../../../shared/tokenDecode";

const EditRecipe = ({ authToken, identity, match }) => {
  const [recipe, dispatchRecipe] = useReducer(recipeReducer, newRecipe());
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(false);
  const [fetched, setFetched] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const result = await axios({
          url: "/recipes/" + match.params.id,
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });
        if (result.data.recipe.author === identity) {
          dispatchRecipe({
            type: "CHANGE",
            data: { ...result.data.recipe },
          });
          setLoading(false);
          setFetched(true);
        } else {
          toast.error("Brak uprawnień do edycji tego przepisu!");
          return <Redirect to={"/myrecipes/"} />;
        }
      } catch (error) {
        axiosError(error);
      }
    };

    if (authToken && !fetched) {
      fetchData();
    }
  }, [authToken, identity, match.params.id, fetched]);

  const submitHandler = async (event) => {
    event.preventDefault();

    setLoading(true);
    try {
      await axios.patch("/recipes/" + recipe.id, recipe, {
        headers: { Authorization: `Bearer ${authToken}` },
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
    return <Redirect to={"/myrecipes/" + recipe.id} />;
  }

  return (
    <AuthRequired>
      <h1>Edytuj przepis</h1>
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
    identity: getIdentity(state.auth.access_token),
  };
};

export default connect(mapStateToProps)(EditRecipe);
