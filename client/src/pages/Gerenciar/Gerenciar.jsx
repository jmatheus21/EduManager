import React from "react";
import { Button, Col, Container, Row } from "react-bootstrap";
import Cabecalho from "../../components/Cabecalho";
import Pagina from "../../components/Pagina";
import { Outlet, useLocation, useNavigate } from "react-router-dom";

/**
 * Componente de template para as páginas de 'Gerenciar'
 * Este componente padroniza o cabeçalho e o menu lateral em todas as páginas de 'Gerenciar'.
 *
 * @returns {JSX.Element} O componente de template de 'Gerenciar'.
 */
const Gerenciar = ({ menus }) => {
  const navigate = useNavigate();
  const url = useLocation();

  return (
    <Pagina>
      <Cabecalho menus={menus} />
      <Container fluid className="flex-fill d-flex">
        <Row lg={"auto"} className="flex-fill">
          <Col
            lg={3}
            className="bg-primary bg-opacity-50 d-none d-lg-flex justify-content-end align-items-center col-0"
          >
            <div className="d-flex flex-column gap-3 w-75">
              <Button
                variant="light"
                className="py-2 nav-button"
                onClick={() => navigate("/")}
              >
                Página Inicial
              </Button>
              {
                menus.map((menu, index) => (
                  <Button
                    key={index}
                    variant={url.pathname === menu.url ? "primary" : "light"}
                    className={`${url.pathname === menu.url ? "bg-primary" : ""} py-2 nav-button`}
                    onClick={() => navigate(menu.url)}
                  >
                    {menu.nome}
                  </Button>
                ))
              }
            </div>
          </Col>
          <Col lg={9} className="px-5 py-4 d-flex col-12">
            <Outlet className="flex-fill" />
          </Col>
        </Row>
      </Container>
    </Pagina>
  );
};

export default Gerenciar;
