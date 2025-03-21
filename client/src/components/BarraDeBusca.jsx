import React, { useState, useEffect } from "react";
import { Alert, Button, Container, Form } from "react-bootstrap";
import useApi from "../hooks/useApi.jsx";
import { useLocation, useNavigate } from "react-router-dom";

/**
 * Componente unificado para barra de busca e exibição de alertas.
 * Este componente combina a funcionalidade de busca da BarraDeBusca e a exibição de alertas do Alerta.
 *
 * @param {Object} props - Propriedades do componente.
 * @param {string} props.atributoNome - Nome do atributo que será buscado (ex.: "Número").
 * @param {string} props.tipo - Tipo do campo de busca (ex.: "number" ou "text").
 * @param {string} props.placeholder - Placeholder do campo de busca.
 * @param {number} props.min - Valor mínimo para campos do tipo número.
 * @param {number} props.max - Valor máximo para campos do tipo número.
 * @param {number} props.minLength - Comprimento mínimo para campos do tipo texto.
 * @param {number} props.maxLength - Comprimento máximo para campos do tipo texto.
 * @param {string} props.entidade - Nome da entidade que está sendo buscada (ex.: "sala").
 * @returns {JSX.Element} O componente unificado de busca e alerta.
 */
const BarraDeBusca = ({
  atributoNome,
  tipo,
  placeholder,
  min,
  max,
  minLength,
  maxLength,
  rota,
  entidade,
}) => {
  const [chave, setChave] = useState(1);
  const [mensagemAlerta, setMensagemAlerta] = useState("");
  const [tipoAlerta, setTipoAlerta] = useState(""); // "success" ou "danger"
  const api = useApi("/api");
  const navigate = useNavigate();
  const location = useLocation();

  // Verifica se há uma mensagem de sucesso na URL
  const queryParams = new URLSearchParams(location.search);
  const successParam = queryParams.get("success");
  const typeParam = queryParams.get("type");

  // Exibe mensagem de sucesso se houver
  useEffect(() => {
    if (successParam) {
      setTipoAlerta("success");
      setMensagemAlerta(
        typeParam === "remocao"
          ? `${entidade.charAt(0).toUpperCase() + entidade.slice(1)} removid${entidade.endsWith("a") ? "a" : "o"} com sucesso!`
          : `${entidade.charAt(0).toUpperCase() + entidade.slice(1)} cadastrad${entidade.endsWith("a") ? "a" : "o"} com sucesso!`
      );
    }
  }, [successParam, typeParam, entidade]);

  /**
   * Função para realizar a busca e navegar para a página de detalhes.
   */
  const funcaoBusca = async (event) => {
    event.preventDefault();

    try {
      const response = await api.fetchData(`/${rota}/${chave}`);

      if (response) {
        navigate(`/${rota}/${chave}`);
      }
    } catch (error) {
      setTipoAlerta("danger");
      setMensagemAlerta(
        `${entidade.charAt(0).toUpperCase() + entidade.slice(1)} ${chave} não foi encontrad${entidade.endsWith("a") ? "a" : "o"}`
      );
    }
  };

  const mudarEstado = (event) => {
    setChave(event.target.value);
  };

  return (
    <Container fluid>
      <Form className="d-flex my-4">
        <Form.Label htmlFor="atributo" style={{ whiteSpace: "nowrap" }} className="pe-2 d-flex align-items-center">
          {atributoNome}:{" "}
        </Form.Label>
        {tipo === "number" ? (
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

      {mensagemAlerta && (
        <Alert variant={tipoAlerta} className="p-3 mb-3">
          {mensagemAlerta}
        </Alert>
      )}
    </Container>
  );
};

export default BarraDeBusca;