import React, { useReducer } from "react";

import RecipeForm from "../RecipeForm/RecipeForm";
import recipeReducer from "../../utils/recipeReducer";
import { newPendingRecipe } from "../../utils/baseRecipeObjects";

const InnerEditRecipe = ({ initRecipe, loading, patchRecipe }) => {
  const [recipe, dispatchRecipe] = useReducer(recipeReducer, {
    ...newPendingRecipe(),
    ...initRecipe,
  });

  return (
    <RecipeForm
      recipe={recipe}
      loading={loading}
      onSubmit={(event) => patchRecipe(event, recipe)}
      dispatchRecipe={dispatchRecipe}
    />
  );
};

export default InnerEditRecipe;
