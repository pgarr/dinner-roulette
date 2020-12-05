import { useState } from "react";

import useDebouncedEffect from "./useDebouncedEffect";

// 'validate' function has to return {valid: Boolean, errors: [String]}
// check src\components\Auth\Register\validators.js
const useFormFieldDebouncedValidation = (validate, initialValue = "") => {
  const [value, setValue] = useState(initialValue);
  const [touched, setTouched] = useState(false);
  const [valid, setValid] = useState(false);
  const [errors, setErrors] = useState([]);

  const validationDelay = 1000;

  const setTouchedValue = (val) => {
    setTouched(true);
    setValue(val);
  };

  useDebouncedEffect(
    () => {
      if (touched) {
        const result = validate(value);
        setValid(result.valid);
        setErrors(result.errors);
      }
    },
    validationDelay,
    [value]
  );

  return [{ value, touched, valid, errors }, setTouchedValue];
};

export default useFormFieldDebouncedValidation;
