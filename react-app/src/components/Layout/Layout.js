import React from "react";
import { Col, Container, Row } from "react-bootstrap";
import { Flip, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import styles from "./Layout.module.css";
import Toolbar from "../Toolbar/Toolbar";

const Layout = ({ children }) => (
  <Container fluid>
    <Row>
      <Col className={styles.NavbarContainer}>
        <Toolbar />
      </Col>
    </Row>
    <Row>
      <Col>
        <main className={styles.Content}>{children}</main>
      </Col>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        transition={Flip}
      />
    </Row>
  </Container>
);

export default Layout;
