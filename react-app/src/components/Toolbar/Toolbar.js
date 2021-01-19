import React from "react";
import { Nav, Navbar } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import UserDropdown from "./UserDropdown/UserDropdown";

const Toolbar = () => (
  <Navbar collapseOnSelect bg="dark" variant="dark" expand="lg">
    <Navbar.Brand href="/">Cookbook</Navbar.Brand>
    <Navbar.Toggle aria-controls="responsive-navbar-nav" />
    <Navbar.Collapse id="responsive-navbar-nav">
      <Nav className="mr-auto">
        <Nav.Link href="/recipes">Przepisy</Nav.Link>
        <Nav.Link href="/newrecipe">
          <FontAwesomeIcon icon="plus" /> Dodaj przepis
        </Nav.Link>
      </Nav>
      <Nav>
        <UserDropdown />
      </Nav>
    </Navbar.Collapse>
  </Navbar>
);

export default Toolbar;
