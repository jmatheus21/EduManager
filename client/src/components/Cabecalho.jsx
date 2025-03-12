import React, { useState } from "react";
import { Button, Container, Nav, Navbar, Offcanvas } from "react-bootstrap";
import { FaBars } from "react-icons/fa";
import { IoLogOutOutline } from "react-icons/io5";
import { useLocation } from "react-router-dom";

/**
 * Componente para exibir o cabeçalho da página.
 * Este componente permite visualizar o cabeçalho da página e ele também exibe um menu sanduíche em telas menores.
 *
 * @returns {JSX.Element} O componente de cabeçalho.
 */
const Cabecalho = ({ menus }) => {
  const [showMenu, setShowMenu] = useState(false);
  const url = useLocation();

  return (
    <div>
      <Navbar bg="primary" variant="dark" expand="lg" className="p-3">
        <Container fluid>
          <Button
            className="d-lg-none text-light"
            onClick={() => setShowMenu(!showMenu)}
          >
            <FaBars size={24} />
          </Button>

          <Navbar.Brand href="/" className="fs-2 fw-bold">
            EduManager
          </Navbar.Brand>

          <Navbar.Collapse className="justify-content-end d-none d-lg-flex">
            <Nav className="d-flex align-items-center gap-3">
              <p className="text-light">username</p>
              <Nav.Link href="/" className="text-light">
                <IoLogOutOutline size={30} />
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <Offcanvas
        show={showMenu}
        onHide={() => setShowMenu(false)}
        placement="start"
        className="p-3"
      >
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>Menu</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <Nav className="flex-column gap-3 pt-3">
            {url.pathname == "/" ? (
              ""
            ) : (
              <Nav.Link href="/" onClick={() => setShowMenu(false)}>
                Página Inicial
              </Nav.Link>
            )}
            {menus?.map((menu, index) => (
              <Nav.Link
                key={index}
                href={menu.url}
                onClick={() => setShowMenu(false)}
              >
                {menu.nome}
              </Nav.Link>
            ))}
            <Nav.Link href="/" onClick={() => setShowMenu(false)}>
              Sair
            </Nav.Link>
          </Nav>
        </Offcanvas.Body>
      </Offcanvas>
    </div>
  );
};

export default Cabecalho;
