import React, { useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import useApi from "../../hooks/useApi";
import { useLocation, useNavigate, useParams } from "react-router";
import { Titulo } from "../../components";
import Formulario from "./components/Formulario";

/**
 * Componente para cadastrar ou alterar um usuário.
 * Este componente permite ao usuário cadastrar um novo usuario ou alterar os dados de um usuário existente.
 * 
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar um usuário.
 */
const FormularioUsuario = () => {
  // Configuração padrão
  const [alterar, setAlterar] = useState(false);
  const [dados, setDados] = useState({});
  const { createData, updateData, fetchData, loading, error } = useApi("/api");
  const url = useLocation();
  const navigate = useNavigate();
  const { chave } = useParams();

  /**
   * Efeito para carregar os dados do usuário quando o componente é montado ou quando o caminho da URL ou o parâmetro `chave` mudam.
   * Se o caminho da URL incluir "alterar", o título do formulário será alterado para "Alterar" e os dados do usuário serão carregados.
   */
  useEffect(() => {
    const verificarURL = async () => {
      if (url.pathname.includes("alterar")) {
        setAlterar(true);

        try {
          const response = await fetchData(`/usuario/${chave}`);
          if (response) setDados(response);
        } catch (error) {
          console.error("Erro ao carregar dados do usuário:", error);
        }
      }
    };
  
    verificarURL();
  }, [url.pathname, chave]);

  /**
   * Função para lidar com o envio do formulário.
   * Dependendo do caminho da URL, a função irá cadastrar um novo usuário ou alterar um usuário existente.
   * 
   * @param {Event} event - O evento de submissão do formulário.
   */
  const enviarFormulario = async (data) => {

    // garantir que a chave primária não altera
    if (alterar) data["cpf"] = chave;

    data.cpf = data.cpf.replace(/\D/g, '');
    data.disciplinas = data.disciplinas.split(',').map((disciplina) => disciplina.trim());

    try {
      if (alterar) {
        await updateData(`/usuario/${chave}`, data);

        navigate(`/usuario/${chave}?success=true`);
      } else {
        await createData("/usuario", data);

        navigate("/usuario?success=true&type=cadastro");
      }
    } catch (error) {
      throw new Error(error.message);
    }
  };
  
    // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
    if (alterar && loading) return <p>Carregando...</p>;
  
    // Exibe mensagem de erro caso ocorra um erro na requisição
    if (alterar && error) return <p>Erro: {error}</p>;
  
    return (
      <Container fluid className="d-flex flex-column h-100 overflow-y-auto">
        <Titulo>{alterar? "Alterar" : "Cadastrar"} Usuário</Titulo>
        <Formulario enviarFormulario={enviarFormulario} alteracao={{alterar: alterar, dados: dados, chave: chave}} />
      </Container>
    );
  };
  
  export default FormularioUsuario;