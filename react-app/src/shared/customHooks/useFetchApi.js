import { useEffect, useState, useReducer } from "react";

import axios from "../axios-api";

const useFetchApi = (initialRequest, initialData, shouldFetch = true) => {
  const [request, setRequest] = useState(initialRequest);

  const [state, dispatch] = useReducer(dataFetchReducer, {
    isLoading: false,
    isError: false,
    data: initialData,
  });

  useEffect(() => {
    let cancelled = false;

    const fetchData = async () => {
      dispatch({ type: "FETCH_INIT" });

      try {
        const result = await axios(request);

        if (!cancelled) {
          dispatch({ type: "FETCH_SUCCESS", payload: result.data });
        }
      } catch (error) {
        if (!cancelled) {
          dispatch({ type: "FETCH_FAILURE" });
        }
      }
    };

    if (shouldFetch) {
      fetchData();
    }
    return () => {
      cancelled = true;
    };
  }, [request, shouldFetch]);

  return [state, setRequest];
};

const dataFetchReducer = (state, action) => {
  switch (action.type) {
    case "FETCH_INIT":
      return {
        ...state,
        isLoading: true,
        isError: false,
      };
    case "FETCH_SUCCESS":
      return {
        ...state,
        isLoading: false,
        isError: false,
        data: action.payload,
      };
    case "FETCH_FAILURE":
      return {
        ...state,
        isLoading: false,
        isError: true,
      };
    default:
      throw new Error();
  }
};

export default useFetchApi;
