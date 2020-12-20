export const newRecipe = () => {
  return {
    title: "",
    time: 0,
    difficulty: 0,
    ingredients: [],
    link: "",
    preparation: "",
    id: null,
  };
};

export const newPendingRecipe = () => {
  return {
    title: "",
    time: 0,
    difficulty: 0,
    ingredients: [],
    link: "",
    preparation: "",
    id: null,
    author: "",
    refused: false,
  };
};
