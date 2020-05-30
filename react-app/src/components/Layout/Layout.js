import { Col, Container, Row } from "react-bootstrap";
import React from "react";
import styles from "./Layout.module.css";
import Toolbar from "../Toolbar/Toolbar";

const Layout = (props) => (
  <Container fluid>
    <Row>
      <Col>
        <Toolbar />
      </Col>
    </Row>
    <Row>
      <Col>
        <main className={styles.Content}>{props.children}</main>
      </Col>
    </Row>
  </Container>
);

export default Layout;
