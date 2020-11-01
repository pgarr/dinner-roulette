import React from "react";
import { Button, Form, FormControl, Nav, Navbar } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import UserDropdown from "./UserDropdown/UserDropdown";

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
      <Form inline>
        <FormControl type="text" placeholder="Szukaj" className="mr-sm-2" />
        <Button variant="outline-info">Szukaj</Button>
      </Form>
    </Navbar.Collapse>
  </Navbar>
);

export default Toolbar;
