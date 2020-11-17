import React from "react";
import { Col, Container, Row } from "react-bootstrap";

import styles from "./Layout.module.css";
import Toolbar from "../Toolbar/Toolbar";

const Layout = ({ children }) => (
  <Container fluid>
    <Row>
      <Col>
        <Toolbar />
      </Col>
    </Row>
    <Row>
      <Col>
        <main className={styles.Content}>{children}</main>
      </Col>
    </Row>
  </Container>
);

export default Layout;
