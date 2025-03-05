import React from "react";
import { Button, Container } from "react-bootstrap";

/**
 * Componente para exibir o botão de finalizar cadastro.
 * Este componente permite visualizar um botão de finalizar para finalizar o cadastro de objetos no formulário.
 *
 * @returns {JSX.Element} O componente de botão de finalizar cadastro.
 */
const BotaoCadastrar = () => {
  return (
    <Container fluid className="d-flex justify-content-end mt-auto">
      <Button variant="primary" type="submit" className="py-2 px-3 ms-2 w-auto">
        Finalizar
      </Button>
    </Container>
  );
};

export default BotaoCadastrar;
