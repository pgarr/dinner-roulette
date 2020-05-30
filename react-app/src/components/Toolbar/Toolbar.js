import React from "react";
import {
  Button,
  Form,
  FormControl,
  Nav,
  Navbar,
  NavDropdown,
} from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const Toolbar = (props) => (
  <Navbar bg="dark" variant="dark" expand="lg">
    <Navbar.Brand href="#home">Cookbook</Navbar.Brand>
    <Navbar.Toggle aria-controls="basic-navbar-nav" />
    <Navbar.Collapse id="basic-navbar-nav">
      <Nav className="mr-auto">
        <Nav.Link href="#home">
          <FontAwesomeIcon icon="plus" /> Dodaj przepis
        </Nav.Link>
        <NavDropdown
          title={
            <span>
              <FontAwesomeIcon icon="user" /> User
            </span>
          }
          id="basic-nav-dropdown"
        >
          <NavDropdown.Item href="#action/3.1">Moje przepisy</NavDropdown.Item>
          <NavDropdown.Item href="#action/3.2">
            Oczekujące przepisy
          </NavDropdown.Item>
          <NavDropdown.Divider />
          <NavDropdown.Item href="#action/3.3">Wyloguj się</NavDropdown.Item>
        </NavDropdown>
      </Nav>
      <Form inline>
        <FormControl type="text" placeholder="Szukaj" className="mr-sm-2" />
        <Button variant="outline-info">Szukaj</Button>
      </Form>
    </Navbar.Collapse>
  </Navbar>
);

export default Toolbar;
