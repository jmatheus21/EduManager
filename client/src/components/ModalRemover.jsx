import React from "react";
import { Button, Modal } from "react-bootstrap";
import { Botao } from "./Botao";

/**
 * Componente para exibir modal de remover objeto.
 * Este componente permite visualizar um modal que vai perguntar se o usuário deseja remover o objeto.
 *
 * @returns {JSX.Element} O componente de remoção.
 */
const ModalRemover = ({ estado, funcaoFechar, funcaoRemover, entidade }) => {
  return (
    <Modal centered show={estado} onHide={funcaoFechar}>
      <Modal.Header closeButton className="p-3">
        <Modal.Title>Remover {entidade}</Modal.Title>
      </Modal.Header>
      <Modal.Body className="p-3">
        {typeof(entidade) == 'string'? `Tem certeza que deseja remover ${entidade.endsWith("a")? "a" : "o"} ${entidade.toLowerCase()}?` : entidade}
      </Modal.Body>
      <Modal.Footer className="p-2 d-flex gap-2">
        <Botao.Group>
          <Botao.Base title="Voltar" sx={{ bgcolor: "grey.600", color: "white" }} onClick={funcaoFechar} />
          <Botao.Base title="Confirmar" color="error" onClick={funcaoRemover} />
        </Botao.Group>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalRemover;
