import React from "react";
import { Button, Container } from "react-bootstrap";

/**
 * Componente para exibir os botões de remoção e alteração do objeto.
 * Este componente permite visualizar um botão de remover e outro de alterar para manipulação do objeto.
 *
 * @returns {JSX.Element} O componente de botão de remoção e de alteração.
 */
const BotaoInfo = ({ funcaoRemover, funcaoAlterar }) => {
  return (
    <Container fluid className="d-flex justify-content-end gap-3 mt-auto">
      <Button variant="danger" className="py-2 px-3" onClick={funcaoRemover}>
        Remover
      </Button>
      <Button variant="primary" className="py-2 px-3" onClick={funcaoAlterar}>
        Alterar
      </Button>
    </Container>
  );
};

export default BotaoInfo;
