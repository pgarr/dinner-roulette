import { useReducer } from "react";

const useValueValidation = (initialValue) => {
  const [state, dispatch] = useReducer(valueValidationReducer, {
    value: initialValue,
    touched: false,
    valid: false,
    errors: [],
  });

  return [state, dispatch];
};

const valueValidationReducer = (state, action) => {
  switch (action.type) {
    case "SET_VALUE":
      return {
        ...state,
        value: action.value,
        touched: true,
      };
    case "SET_VALIDATION":
      return {
        ...state,
        valid: action.valid,
        errors: action.errors,
      };
    default:
      throw new Error();
  }
};

export default useValueValidation;
