import React, { useReducer } from "react";
import { Redirect } from "react-router-dom";
import { Form, Button } from "react-bootstrap";

import {
  buildValidationObject,
  validateOnBackend,
  validatePassword,
  validatePassword2,
} from "./validators";
import axios, { isErrorStatus } from "../../../shared/axios-api";
import { inputChangedDispatch } from "../../../shared/handlers";
import useDebouncedEffect from "../../../shared/customHooks/useDebouncedEffect";
import InlineFormField from "../../UI/InlineFormField/InlineFormField";
import ModalWithBackdrop from "../../UI/ModalWithBackdrop/ModalWithBackdrop";
import { axiosError } from "../../../shared/errors";
import AuthForbidden from "../../HOC/AuthForbidden";
import useValueValidation from "../../../shared/customHooks/useValueValidation";

const registerReducer = (state, action) => {
  switch (action.type) {
    case "INIT_REQUEST":
      return {
        ...state,
        validated: false,
        registered: false,
        confirmed: false,
        loading: true,
      };
    case "REQUEST_SUCCESS":
      return { ...state, validated: true, registered: true, loading: false };
    case "REQUEST_FAIL":
      return { ...state, loading: false };
    case "MODAL_CONFIRMED":
      return { ...state, confirmed: true };
    default:
      return { ...state };
  }
};

const Register = () => {
  const [{ validated, registered, confirmed, loading }, dispatch] = useReducer(
    registerReducer,
    {
      validated: false,
      registered: false,
      confirmed: false,
      loading: false,
    }
  );

  const [username, dispatchUsername] = useValueValidation("");
  const [email, dispatchEmail] = useValueValidation("");
  const [password, dispatchPassword] = useValueValidation("");
  const [password2, dispatchPassword2] = useValueValidation("");

  const validationDelay = 1000;

  // validate username and email
  useDebouncedEffect(
    async () => {
      let usernameParam = null;
      let emailParam = null;

      if (username.touched) {
        usernameParam = username.value;
      }
      if (email.touched) {
        emailParam = email.value;
      }

      if (usernameParam !== null || emailParam !== null) {
        const result = await validateOnBackend(usernameParam, emailParam);
        setValidationResults(result);
      }
    },
    validationDelay,
    [username.value, email.value]
  );

  // validate password
  useDebouncedEffect(
    () => {
      if (password.touched) {
        const result = validatePassword(password.value);
        dispatchPassword({ type: "SET_VALIDATION", ...result });
      }
    },
    validationDelay,
    [password.value]
  );

  // validate password2
  useDebouncedEffect(
    () => {
      if (password2.touched) {
        const result = validatePassword2(password.value, password2.value);
        dispatchPassword2({ type: "SET_VALIDATION", ...result });
      }
    },
    validationDelay,
    [password.value, password2.value]
  );

  const setValidationResults = (result) => {
    for (const key in result) {
      switch (key) {
        case "username":
          dispatchUsername({ type: "SET_VALIDATION", ...result[key] });
          break;
        case "email":
          dispatchEmail({ type: "SET_VALIDATION", ...result[key] });
          break;
        case "password":
          dispatchPassword({ type: "SET_VALIDATION", ...result[key] });
          break;
        default:
          break;
      }
    }
  };

  const submitHandler = async (event) => {
    event.preventDefault();
    dispatch({ type: "INIT_REQUEST" });
    try {
      await axios.post("/auth/register", {
        username: username.value,
        password: password.value,
        email: email.value,
      });
      dispatch({ type: "REQUEST_SUCCESS" });
    } catch (error) {
      if (isErrorStatus(error, 422)) {
        const result = buildValidationObject(error.response.data);
        setValidationResults(result);
      } else {
        axiosError(error);
      }
      dispatch({ type: "REQUEST_FAIL" });
    }
  };

  let redirect = null;
  if (confirmed) {
    redirect = <Redirect to={"/login"} />;
  }

  return (
    <AuthForbidden>
      {redirect}

      <ModalWithBackdrop
        show={registered && !confirmed}
        onHide={() => {
          dispatch({ type: "MODAL_CONFIRMED" });
        }}
        title="Sukces!"
        text="Zarejestrowałeś się. Zaloguj się za pomocą podanych danych."
      />

      <h1>Zarejestruj się</h1>
      <Form noValidate validated={validated} onSubmit={submitHandler}>
        <InlineFormField
          controlId="formUsername"
          labelText="Nazwa użytkownika"
          type="text"
          errors={username.errors}
          value={username.value}
          onChangeHandler={(event) => {
            inputChangedDispatch(event, dispatchUsername);
          }}
          isValid={username.touched && username.valid}
          isInvalid={username.touched && !username.valid}
          disabled={loading}
        />
        <InlineFormField
          controlId="formEmail"
          labelText="E-mail"
          type="email"
          errors={email.errors}
          value={email.value}
          onChangeHandler={(event) => {
            inputChangedDispatch(event, dispatchEmail);
          }}
          isValid={email.touched && email.valid}
          isInvalid={email.touched && !email.valid}
          disabled={loading}
        />
        <InlineFormField
          controlId="formPassword"
          labelText="Hasło"
          type="password"
          errors={password.errors}
          value={password.value}
          onChangeHandler={(event) => {
            inputChangedDispatch(event, dispatchPassword);
          }}
          isValid={password.touched && password.valid}
          isInvalid={password.touched && !password.valid}
          disabled={loading}
        />
        <InlineFormField
          controlId="formPassword2"
          labelText="Powtórz hasło"
          type="password"
          errors={password2.errors}
          value={password2.value}
          onChangeHandler={(event) => {
            inputChangedDispatch(event, dispatchPassword2);
          }}
          isValid={password2.touched && password2.valid}
          isInvalid={password2.touched && !password2.valid}
          disabled={loading}
        />
        <Button
          variant="secondary"
          type="submit"
          disabled={
            !username.valid ||
            !email.valid ||
            !password.valid ||
            !password2.valid ||
            loading
          }
        >
          Zarejestruj się
        </Button>
      </Form>
    </AuthForbidden>
  );
};

export default Register;
