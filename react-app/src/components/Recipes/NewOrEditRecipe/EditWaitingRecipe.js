import React, { useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { toast } from "react-toastify";

import useFetchApi from "../../../shared/customHooks/useFetchApi";
import AuthRequired from "../../HOC/AuthRequired";
import LoadingContainer from "../../HOC/LoadingContainer/LoadingContainer";
import axios from "../../../shared/axios-api";
import { axiosError } from "../../../shared/errors";
import { newPendingRecipe } from "../utils/baseRecipeObjects";
import InnerEditRecipe from "./InnerEditRecipe.js/InnerEditRecipe";

const EditWaitingRecipe = ({ isAuthenticated, authToken, match }) => {
  const [{ data, isLoading }] = useFetchApi(
    {
      url: "/waiting/" + match.params.id,
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    },
    {
      pending_recipe: newPendingRecipe(),
    },
    isAuthenticated
  );

  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(false);

  const patchRecipe = async (event, recipe) => {
    event.preventDefault();

    setLoading(true);
    try {
      await axios.patch("/waiting/" + data.pending_recipe.id, recipe, {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
      toast.info(
        "Zmiany będą widoczne dla innych użytkowników po zatwierdzeniu przez administratora."
      );
      setSaved(true);
    } catch (error) {
      axiosError(error);
      setLoading(false);
    }
  };

  if (saved) {
    return <Redirect to={"/pendingrecipes/" + data.pending_recipe.id} />;
  }

  return (
    <AuthRequired>
      <h1>Edytuj przepis</h1>
      <LoadingContainer isLoading={isLoading}>
        <InnerEditRecipe
          initRecipe={data.pending_recipe}
          loading={loading}
          patchRecipe={patchRecipe}
        />
      </LoadingContainer>
    </AuthRequired>
  );
};

const mapStateToProps = (state) => {
  return {
    authToken: state.auth.access_token,
    isAuthenticated: state.auth.access_token !== null,
  };
};

export default connect(mapStateToProps)(EditWaitingRecipe);
