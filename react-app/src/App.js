import React from "react";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faClock,
  faPlus,
  faStar as fasFaStar,
  faUser,
} from "@fortawesome/free-solid-svg-icons";
import { faStar as farFaStar } from "@fortawesome/free-regular-svg-icons";

import Layout from "./components/Layout/Layout";
import RecipesList from "./components/RecipesList/RecipesList";
import RecipeCard from "./components/RecipeCard/RecipeCard";

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

const recipe = {
  title: "Testowy tutuł",
  author: "user",
  time: 15,
  difficulty: 4,
  ingredients: [
    {
      name: "Test",
      amount: 2,
      unit: "kg",
    },
    {
      name: "Test2",
      amount: 2,
      unit: "kg",
    },
    {
      name: "Test3",
      amount: 2,
      unit: "kg",
    },
  ],
  preparation:
    " Lorem asd fdf  sdf sdfsdfsjdflsdjf l dsfsldjf sdfn lsdjf sdfhsjdfhsdfksd sdfhksdfhk shdjfh ksdhfjsdhfkjs sdhfksdfhkdsfhksjhkfjsd hksdfhksd hfksdhfkh",
  link: "http://test",
};

function App() {
  library.add(faClock, faPlus, farFaStar, fasFaStar, faUser);
  return (
    <div>
      <Layout>
        {/* <RecipesList recipes={recipes} /> */}
        <RecipeCard {...recipe} />
      </Layout>
    </div>
  );
}

export default App;
