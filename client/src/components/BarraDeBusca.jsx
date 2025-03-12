import React, { useState } from "react";
import { Alert, Button, Container, Form } from "react-bootstrap";
import useApi from "../hooks/useApi.jsx";
import { useNavigate } from "react-router-dom";

/**
 * Componente para exibir a barra de busca.
 * Este componente permite visualizar uma barra de busca que permite ao usuário buscar o objeto por sua chave primária.
 *
 * @returns {JSX.Element} O componente de busca.
 */
const BarraDeBusca = ({
  atributoNome,
  tipo,
  placeholder,
  min,
  max,
  minLength,
  maxLength,
  entidade
}) => {
  const [chave, setChave] = useState(1);
  const [textAlert, setTextAlert] = useState("");
  const api = useApi("/api");
  const navigate = useNavigate();
  /**
   * Função para navegar para a página de detalhes a chave especificada.
   */
  const funcaoBusca = async (event) => {
    event.preventDefault();

    try {
      const response = await api.fetchData(`/${entidade}/${chave}`);

      if (response) {
        navigate(`/${entidade}/${chave}`);
      }
    } catch (error) {
      if (typeof (entidade) == "string") {
        setTextAlert(`${entidade.charAt(0).toUpperCase() + entidade.slice(1)} ${chave} não foi encontrad${entidade.endsWith("a") ? "a" : "o"}`);
      }
    }
  };

  const mudarEstado = (event) => {
    setChave(event.target.value);
  };

  return (
    <Container fluid>
      <Form className="d-flex my-4">
        <Form.Label htmlFor="atributo" className="pe-2 d-flex align-items-center">
          {atributoNome}:{" "}
        </Form.Label>
        {tipo == "number" ? (
          <Form.Control
            id="atributo"
            type="number"
            placeholder={placeholder}
            className="px-2"
            min={min}
            max={max}
            onChange={mudarEstado}
          />
        ) : (
          <Form.Control
            type={tipo}
            placeholder={placeholder}
            className="px-2"
            minLength={minLength}
            maxLength={maxLength}
            onChange={mudarEstado}
          />
        )}
        <Button
          variant="primary"
          type="submit"
          className="py-2 px-3 ms-2"
          onClick={funcaoBusca}
        >
          Buscar
        </Button>
      </Form>
      {textAlert && (
        <Alert variant="danger" className="p-3 mb-3">
          {textAlert}
        </Alert>
      )}
    </Container>
  );
};

export default BarraDeBusca;
