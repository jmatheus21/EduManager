import React, { useEffect, useState } from "react";
import { Alert, Col, Container, Row } from "react-bootstrap";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Titulo, BotaoInfo, ModalRemover } from "../../components";
import useApi from "../../hooks/useApi";

/**
 * Componente para exibir informações detalhadas de uma turma.
 * Este componente permite visualizar os detalhes de uma turma específico, além de oferecer opções para alterar ou remover a turma.
 *
 * @returns {JSX.Element} O componente de informações da turma.
 */
const InfoTurma = () => {
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
   * Função para remover a turma.
   * Após a remoção bem-sucedida, o usuário é redirecionado para a lista de turmas.
   */
  const RemoverTurma = async () => {
    try {
      await api.deleteData(`/turma/${chave}`);
      navigate("/turma?success=true&type=remocao");
    } catch (error) {
      console.error("Erro ao remover turma:", error);
      alert("Erro ao remover turma, tente novamente mais tarde");
    }
  };

  /**
   * Efeito para buscar os dados da turma ao carregar o componente ou quando o ano letivo da turma muda.
   */
  useEffect(() => {
    api.fetchData(`/turma/${chave}`);
  }, [chave]);

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (api.loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  if (api.error) return <p>Erro: {api.error}</p>;

  return (
    <Container fluid className="d-flex flex-column justify-content-between">
      <Titulo>Informações da Turma</Titulo>
      {successParam && (
        <Alert variant="success" className="p-3 mt-3">
          Turma alterada com sucesso!
        </Alert>
      )}
      <Container fluid className="my-4 d-grid gap-3">
        <Row>
          <Col>
            <h5>Identificação:</h5>
            {api.data && <p data-testid="chave_primaria">{api.data.id}</p>}
          </Col>
          <Col>
            <h5>Ano letivo:</h5>
            {api.data && <p>{api.data.calendario_ano_letivo}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Ano:</h5>
            {api.data && <p>{api.data.ano}</p>}
          </Col>
          <Col>
            <h5>Série:</h5>
            {api.data && <p>{api.data.serie}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Nível de Ensino:</h5>
            {api.data && <p>{api.data.nivel_de_ensino}</p>}
          </Col>
          <Col>
            <h5>Turno:</h5>
            {api.data && <p>{api.data.turno}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Status:</h5>
            {api.data && <p>{api.data.status}</p>}
          </Col>
          <Col>
            <h5>Sala:</h5>
            {api.data && <p>{api.data.sala_numero}</p>}
          </Col>
        </Row>
      </Container>
      <BotaoInfo
        funcaoAlterar={() => navigate(`/turma/alterar/${chave}`)}
        funcaoRemover={handleShow}
      />
      <ModalRemover
        estado={show}
        funcaoFechar={handleClose}
        funcaoRemover={RemoverTurma}
        entidade={"Turma"}
      />
    </Container>
  );
};

export default InfoTurma;
