export const inputChangedHandler = (event, setValue) => {
  setValue(event.target.value);
};

export const inputTouchedChangedHandler = (event, setValue) => {
  setValue({ value: event.target.value, touched: true });
};
