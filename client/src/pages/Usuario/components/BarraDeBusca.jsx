import React, { useState, useEffect } from "react";
import { Button, Container, Form } from "react-bootstrap";
import useApi from "../../../hooks/useApi.jsx";
import { useLocation, useNavigate } from "react-router-dom";
import { IMaskInput } from "react-imask";
import { Alert } from "@mui/material";
import { Botao } from "../../../components/Botao/index.jsx";

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
      const response = await api.fetchData(`/usuario/cpf/${chave}`);

      if (response) {
        navigate(`/usuario/${response.id}`);
      }
    } catch (error) {
      setTipoAlerta("error");
      setMensagemAlerta(
        `Usuário com CPF ${chave} não foi encontrado`
      );
    }
  };

  const mudarEstado = (event) => {
    setChave(event.target.value.replace(/\D/g, ''));
  };

  return (
    <Container fluid>
      <Form className="d-flex my-4">
        <Form.Label htmlFor="atributo" style={{ whiteSpace: "nowrap" }} className="pe-2 d-flex align-items-center">
          <p>CPF: </p>
        </Form.Label>
        <IMaskInput
            mask={"000.000.000-00"}
            id="atributo"   
            type="text"
            placeholder="Exemplo: 999.888.777-66"
            className="px-2 form-control me-3"
            onChange={mudarEstado}
        />
        <Botao.Base
          title="Buscar"
          type="submit"
          onClick={funcaoBusca}
        />
      </Form>

      {mensagemAlerta && (
        <Alert severity={tipoAlerta} className="p-3 mb-3 d-flex align-content-center gap-3">
          {mensagemAlerta}
        </Alert>
      )}
    </Container>
  );
};

export default BarraDeBusca;