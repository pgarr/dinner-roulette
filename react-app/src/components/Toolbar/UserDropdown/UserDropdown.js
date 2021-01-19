import React from "react";
import { connect } from "react-redux";
import { NavDropdown, Nav } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { getIdentity } from "../../../shared/tokenDecode";

const UserDropdown = ({ identity }) => {
  if (!identity) {
    return (
      <Nav.Link bg="dark" variant="dark" href="/login">
        Zaloguj się
      </Nav.Link>
    );
  } else {
    return (
      <NavDropdown
        alignRight
        title={
          <span>
            <FontAwesomeIcon icon="user" /> {identity}
          </span>
        }
        id="basic-nav-dropdown"
      >
        <NavDropdown.Item href="/myrecipes">Moje przepisy</NavDropdown.Item>
        <NavDropdown.Divider />
        <NavDropdown.Item href="/logout">Wyloguj się</NavDropdown.Item>
      </NavDropdown>
    );
  }
};

const mapStateToProps = (state) => {
  return {
    identity: getIdentity(state.auth.access_token),
  };
};

export default connect(mapStateToProps, null)(UserDropdown);
