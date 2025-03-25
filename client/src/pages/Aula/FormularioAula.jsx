import React, { useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import useApi from "../../hooks/useApi";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Titulo } from "../../components";
import Formulario from "./components/Formulario";

/**
 * Componente para cadastrar ou alterar uma aula.
 * Este componente permite ao usuário cadastrar uma nova aula ou alterar os dados de uma aula existente.
 * 
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar uma aula.
 */
const FormularioAula = () => {
  // Configuração padrão
  const [alterar, setAlterar] = useState(false);
  const [dados, setDados] = useState({});
  const { fetchData, updateData, createData, loading, error } = useApi("/api");
  const navigate = useNavigate();
  const url = useLocation();
  const { chave } = useParams();

  /**
   * Efeito para carregar os dados da aula quando o componente é montado ou quando o caminho da URL ou o parâmetro `chave` mudam.
   * Se o caminho da URL incluir "alterar", o título do formulário será alterado para "Alterar" e os dados da aula serão carregados.
   */
  useEffect(() => {
    const carregarDados = async () => {
      if (url.pathname.includes("alterar")) {
        setAlterar(true);

        try {
          const response = await fetchData(`/aula/${chave}`);
          if (response) setDados(response);
        } catch (error) {
          console.error("Erro ao carregar dados da aula:", error);
        }
      }
    };

    carregarDados();
  }, [url.pathname, chave]);

  /**
   * Função para lidar com o envio do formulário.
   * Dependendo do caminho da URL, a função irá cadastrar uma nova aula ou alterar uma aula existente.
   * 
   * @param {Event} event - O evento de submissão do formulário.
   */
  const enviarFormulario = async (data) => {

    data.usuario_cpf = data.usuario_cpf.replace(/\D/g, '');
 
    try {
      if (alterar) {
        // garantir que a chave primária não foi alterada
        data["id"] = Number(chave);

        await updateData(`/aula/${chave}`, data);

        navigate(`/aula/${data.id}?success=true`);
      } else {
        await createData("/aula", data);

        navigate("/aula?success=true&type=cadastro");
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
      <Titulo>{alterar? "Alterar" : "Cadastrar"} Aula</Titulo>
      <Formulario enviarFormulario={enviarFormulario} alteracao={{alterar: alterar, dados: dados, chave: chave}} />
    </Container>
  );
};

export default FormularioAula;
