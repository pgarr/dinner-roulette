import React from "react";
import { connect } from "react-redux";
import { NavDropdown, Nav } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { getIdentity } from "../../../shared/tokenDecode";

const UserDropdown = ({ identity }) => {
  let userDropdown = <Nav.Link href="/login">Zaloguj się</Nav.Link>;
  if (identity) {
    userDropdown = (
      <NavDropdown
        title={
          <span>
            <FontAwesomeIcon icon="user" /> {identity}
          </span>
        }
        id="basic-nav-dropdown"
      >
        <NavDropdown.Item href="/myrecipes">Moje przepisy</NavDropdown.Item>
        <NavDropdown.Item href="/pendingrecipes">
          Niezatwierdzone przepisy
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
    identity: getIdentity(state.auth.access_token),
  };
};

export default connect(mapStateToProps, null)(UserDropdown);
