import React from "react";
import { Button, Modal } from "react-bootstrap";

/**
 * Componente para exibir modal de erro ao remover sala.
 * Este componente permite visualizar um modal que vai exibir mensagem de erro se o usuário deseja remover a sala.
 *
 * @returns {JSX.Element} O componente de remoção com erro.
 */
const ModalRemoverSalaErro = ({ estado, funcaoFechar }) => {
  return (
    <Modal centered show={estado} onHide={funcaoFechar}>
      <Modal.Header closeButton className="p-3">
        <Modal.Title className="text-danger">Erro ao remover sala</Modal.Title>
      </Modal.Header>
      <Modal.Body className="p-3">
        <p>A sala está associada a uma ou mais turmas ativas.</p>
        <p>Encerre as turmas ou altere a sala delas antes de remover essa sala.</p>
      </Modal.Body>
      <Modal.Footer className="p-2 d-flex gap-2">
        <Button variant="secondary" onClick={funcaoFechar} className="p-2">
          Voltar
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalRemoverSalaErro;