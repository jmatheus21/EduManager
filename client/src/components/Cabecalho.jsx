import React, { useEffect, useState } from "react";
import { Button, Container, Nav, Navbar, Offcanvas } from "react-bootstrap";
import { FaBars } from "react-icons/fa";
import { IoLogOutOutline } from "react-icons/io5";
import { useLocation, useNavigate } from "react-router-dom";
import apiClient from "../axiosConfig";
import { useAuth } from "../contexts/AuthContext";

/**
 * Componente para exibir o cabeçalho da página.
 * Este componente permite visualizar o cabeçalho da página e ele também exibe um menu sanduíche em telas menores.
 *
 * @returns {JSX.Element} O componente de cabeçalho.
 */
const Cabecalho = ({ menus }) => {
  const [showMenu, setShowMenu] = useState(false);
  const url = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();

  const logout = async (e) => {
    e.preventDefault();
    
    try {
      await apiClient("/api/auth/logout");

      navigate("/login");
    } catch (erro) {
      console.erro(erro.message)
    }
  }

  return (
    <div>
      <Navbar bg="primary" variant="dark" expand="lg" className="p-2">
        <Container fluid>
          <Button
            className="d-lg-none text-light"
            onClick={() => setShowMenu(!showMenu)}
          >
            <FaBars size={24} />
          </Button>

          <Navbar.Brand href="/" className="fs-3 fw-bold">
            EduManager
          </Navbar.Brand>

          <Navbar.Collapse className="justify-content-end d-none d-lg-flex">
            <Nav className="d-flex align-items-center gap-3">
              <p className="text-light">{user ? user.nome : "Carregando..."}</p>
              <Nav.Link onClick={logout} className="text-light">
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
