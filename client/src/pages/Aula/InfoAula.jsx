import React, { useEffect, useState } from "react";
import { Alert, Col, Container, Row } from "react-bootstrap";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Titulo, BotaoInfo, ModalRemover } from "../../components";
import useApi from "../../hooks/useApi";

/**
 * Componente para exibir informações detalhadas de uma aula.
 * Este componente permite visualizar os detalhes de uma aula em específico, além de oferecer opções para alterar ou remover a aula.
 *
 * @returns {JSX.Element} O componente de informações da aula.
 */
const InfoAula = () => {
  // Configuração padrão
  const { chave } = useParams();
  const navigate = useNavigate();
  const url = useLocation();
  const queryParams = new URLSearchParams(url.search);
  const successParam = queryParams.get("success");
  const [show, setShow] = useState(false);
  const api = useApi("/api");

  /**
   * Função para fechar o modal de confirmação de remoção.
   */
  const handleClose = () => setShow(false);

  /**
   * Função para abrir o modal de confirmação de remoção.
   */
  const handleShow = () => setShow(true);

  /**
   * Função para remover a aula.
   * Após a remoção bem-sucedida, o usuário é redirecionado para a lista de aulas.
   */
  const RemoverAula = async () => {
    try {
      await api.deleteData(`/aula/${chave}`);
      navigate("/aula?success=true&type=remocao");
    } catch (error) {
      console.error("Erro ao remover aula:", error);
      alert("Erro ao remover aula, tente novamente mais tarde");
    }
  };

  
  /**
   * Efeito para buscar os dados da aula ao carregar.
   */
  useEffect(() => {
    api.fetchData(`/aula/${chave}`);
  }, [chave]);

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (api.loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  if (api.error) return <p>Erro: {api.error}</p>;

  const exibirDiasDaSemana = (dias_da_semana) => {
    return dias_da_semana.map((item, index) => {
      if (dias_da_semana.length == 1 || (dias_da_semana.length - 1) == index) {
        return (<span key={index}>{item.nome} {item}</span>)
      } else if ((dias_da_semana.length - 2) == index) {
        return (<span key={index}>{item.nome} {item} e </span>)
      } else {
        return (<span key={index}>{item.nome} {item}, </span>)
      }
    })
  }

  return (
    <Container fluid className="d-flex flex-column justify-content-between">
      <Titulo>Informações da Aula</Titulo>
      {successParam && (
        <Alert variant="success" className="p-3 mt-3">
          Aula alterada com sucesso!
        </Alert>
      )}
      <Container fluid className="my-4 d-grid gap-3">
        <Row>
          <Col>
            <h5>Identificação:</h5>
              {api.data && <p data-testid="chave_primaria">{api.data.id}</p>}
          </Col>
          <Col>
            <h5>Turma:</h5>
              {api.data && `${api.data.turma_ano}° ano ${api.data.turma_serie} - ${api.data.turma_nivel_de_ensino} (${api.data.turma_id})`}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Professor:</h5>
            {api.data && `${api.data.professor_nome} (${api.data.professor_cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4')})`}
          </Col>
          <Col>
            <h5>Disciplina:</h5>
              {api.data && <p>{api.data.disciplina_nome}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Horário de Início:</h5>
              {api.data && <p>{api.data.hora_inicio.split(":").slice(0, 2).join(":")}</p>}
          </Col>
          <Col>
            <h5>Horário do Fim:</h5>
              {api.data && <p>{api.data.hora_fim.split(":").slice(0, 2).join(":")}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Dias da Semana:</h5>
            {api.data?.dias_da_semana && exibirDiasDaSemana(api.data.dias_da_semana)}
          </Col>
        </Row>
      </Container>
      <BotaoInfo
        funcaoAlterar={() => navigate(`/aula/alterar/${chave}`)}
        funcaoRemover={handleShow}
      />
      <ModalRemover
        estado={show}
        funcaoFechar={handleClose}
        funcaoRemover={RemoverAula}
        entidade={"Aula"}
      />
    </Container>
  );
};

export default InfoAula;