import React from "react";
import { Pagination } from "react-bootstrap";

const NumberedPagination = ({ activePage, totalPages, onChangePage }) => {
  let items = [];
  for (let number = 1; number <= totalPages; number++) {
    items.push(
      <Pagination.Item
        key={number}
        active={number === activePage}
        onClick={
          number === activePage
            ? null
            : (event) => onChangePage(event.target.text)
        }
      >
        {number}
      </Pagination.Item>
    );
  }

  return <Pagination size="sm">{items}</Pagination>;
};

export default NumberedPagination;
