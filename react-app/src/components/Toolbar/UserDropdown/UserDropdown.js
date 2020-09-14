import React from "react";
import { connect } from "react-redux";
import { NavDropdown, Nav } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import jwt from "jsonwebtoken";

const UserDropdown = ({ payload }) => {
  let userDropdown = <Nav.Link href="/login">Zaloguj się</Nav.Link>;
  if (payload) {
    userDropdown = (
      <NavDropdown
        title={
          <span>
            <FontAwesomeIcon icon="user" /> {payload.identity}
          </span>
        }
        id="basic-nav-dropdown"
      >
        <NavDropdown.Item href="#action/3.1">Moje przepisy</NavDropdown.Item>
        <NavDropdown.Item href="#action/3.2">
          Oczekujące przepisy
        </NavDropdown.Item>
        <NavDropdown.Divider />
        <NavDropdown.Item href="/logout">Wyloguj się</NavDropdown.Item>
      </NavDropdown>
    );
  }

  return userDropdown;
};

const mapStateToProps = (state) => {
  return {
    payload:
      state.auth.access_token !== null
        ? jwt.decode(state.auth.access_token)
        : null,
  };
};

export default connect(mapStateToProps, null)(UserDropdown);
