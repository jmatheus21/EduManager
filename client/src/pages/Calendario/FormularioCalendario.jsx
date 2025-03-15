import React, { useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import useApi from "../../hooks/useApi";
import { useLocation, useNavigate, useParams } from "react-router";
import { Titulo } from "../../components";
import Formulario from "./components/Formulario";

/**
 * Componente para cadastrar ou alterar um calendário.
 * Este componente permite ao usuário cadastrar um novo calendário ou alterar os dados de um calendário existente.
 * 
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar um calendário.
 */
const FormularioCalendario = () => {
  // Configuração padrão
  const [alterar, setAlterar] = useState(false);
  const [dados, setDados] = useState({});
  const { fetchData, updateData, createData, loading, error } = useApi("/api");
  const navigate = useNavigate();
  const url = useLocation();
  const { chave } = useParams();

  /**
   * Efeito para carregar os dados do calendário quando o componente é montado ou quando o caminho da URL ou o parâmetro `chave` mudam.
   * Se o caminho da URL incluir "alterar", o título do formulário será alterado para "Alterar" e os dados do calendário serão carregados.
   */
  useEffect(() => {
    const carregarDados = async () => {
      if (url.pathname.includes("alterar")) {
        setAlterar(true);

        try {
          const response = await fetchData(`/calendario/${chave}`);
          if (response) setDados(response);
        } catch (error) {
          console.error("Erro ao carregar dados do calendario:", error);
        }
      }
    };

    carregarDados();
  }, [url.pathname, chave]);

  /**
   * Função para lidar com o envio do formulário.
   * Dependendo do caminho da URL, a função irá cadastrar um novo calendário ou alterar um calenário existente.
   * 
   * @param {Event} event - O evento de submissão do formulário.
   */
  const enviarFormulario = async (data) => {
 
    try {
      if (alterar) {
        // garantir que chave primária não é alterada
        data["ano_letivo"] = Number(chave)

        await updateData(`/calendario/${chave}`, data);

        navigate(`/calendario/${data.ano_letivo}?success=true`);
      } else {
        await createData("/calendario", data);

        navigate("/calendario?success=true&type=cadastro");
      }
    } catch (error) {
      throw error;
    }
  };

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (alterar && loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  if (alterar && error) return <p>Erro: {error}</p>;

  return (
    <Container fluid className="d-flex flex-column">
      <Titulo>{alterar? "Alterar" : "Cadastrar"} Calendário</Titulo>
      <Formulario enviarFormulario={enviarFormulario} alteracao={{ alterar: alterar, dados: dados, chave: chave}} />
    </Container>
  );
};

export default FormularioCalendario;