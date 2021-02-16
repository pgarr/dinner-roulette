import { v4 as uuidv4 } from "uuid";

const newIngredient = () => ({ id: uuidv4(), title: "", amount: "", unit: "" });

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

export default recipeReducer;
