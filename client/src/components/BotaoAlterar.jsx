import React from "react";
import { Button, Container } from "react-bootstrap";

/**
 * Componente para exibir os botões de alterar e voltar.
 * Este componente permite visualizar os botões de alterar e voltarr.
 *
 * @returns {JSX.Element} O componente de botões de alterar e voltar.
 */
const BotaoAlterar = ({ funcaoVoltar }) => {
  return (
    <Container fluid className="d-flex justify-content-end gap-3 mt-auto">
      <Button
        variant="secondary"
        type="button"
        className="py-2 px-3"
        onClick={funcaoVoltar}
      >
        Voltar
      </Button>
      <Button variant="primary" type="submit" className="py-2 px-3">
        Alterar
      </Button>
    </Container>
  );
};

export default BotaoAlterar;
