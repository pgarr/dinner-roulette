import React from "react";
import { Nav, Navbar } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import UserDropdown from "./UserDropdown/UserDropdown";
import SearchWidget from "../Search/SearchWidget";

const Toolbar = () => (
  <Navbar bg="dark" variant="dark" expand="lg">
    <Navbar.Brand href="/">Cookbook</Navbar.Brand>
    <Navbar.Toggle aria-controls="basic-navbar-nav" />
    <Navbar.Collapse id="basic-navbar-nav">
      <Nav className="mr-auto">
        <Nav.Link href="/newrecipe">
          <FontAwesomeIcon icon="plus" /> Dodaj przepis
        </Nav.Link>
        <UserDropdown />
      </Nav>
      <SearchWidget />
    </Navbar.Collapse>
  </Navbar>
);

export default Toolbar;
