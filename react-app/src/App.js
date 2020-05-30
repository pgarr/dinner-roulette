import React from "react";
import Layout from "./components/Layout/Layout";
import RecipesList from "./components/RecipesList/RecipesList";

const recipes = [
  {
    id: 0,
    title: "Test1",
    time: 15,
    difficulty: 4,
  },
  {
    id: 1,
    title: "Test2",
    time: 10,
    difficulty: 5,
  },
];

function App() {
  return (
    <div>
      <Layout>
        <RecipesList recipes={recipes} />
      </Layout>
    </div>
  );
}

export default App;
