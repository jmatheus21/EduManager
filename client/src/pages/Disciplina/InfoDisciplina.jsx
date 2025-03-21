import React, { useEffect, useState } from "react";
import { Alert, Col, Container, Row } from "react-bootstrap";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Titulo, BotaoInfo, ModalRemover } from "../../components";
import useApi from "../../hooks/useApi";

/**
 * Componente para exibir informações detalhadas de uma disciplina.
 * Este componente permite visualizar os detalhes de uma disciplina específica, além de oferecer opções para alterar ou remover a disciplina.
 *
 * @returns {JSX.Element} O componente de informações da disciplina.
 */
const InfoDisciplina = () => {
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
   * Função para remover a disciplina.
   * Após a remoção bem-sucedida, o usuário é redirecionado para a lista de disciplinas.
   */
  const RemoverDisciplina = async () => {
    try {
      await api.deleteData(`/disciplina/${chave}`);
      navigate("/disciplina?success=true&type=remocao");
    } catch (error) {
      console.error("Erro ao remover disciplina:", error);
      alert("Erro ao remover disciplina, tente novamente mais tarde");
    }
  };

  /**
   * Efeito para buscar os dados da disciplina ao carregar o componente ou quando o ano letivo do calendário muda. (necessário?)
   */
  useEffect(() => {
    api.fetchData(`/disciplina/${chave}`);
  }, [chave]);

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (api.loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  if (api.error) return <p>Erro: {api.error}</p>;

  return (
    <Container fluid className="d-flex flex-column justify-content-between">
      <Titulo>Informações da Disciplina</Titulo>
      {successParam && (
        <Alert variant="success" className="p-3 mt-3">
          Disciplina alterada com sucesso!
        </Alert>
      )}
      <Container fluid className="my-4 d-grid gap-3">
        <Row>
          <Col>
            <h5>Nome:</h5>
            {api.data && <p>{api.data.nome}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Código:</h5>
            {api.data && <p data-testid="chave_primaria">{api.data.codigo}</p>}
          </Col>
          <Col>
            <h5>Carga Horária:</h5>
            {api.data && <p>{api.data.carga_horaria}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Ementa:</h5>
            {api.data && <p>{api.data.ementa}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Bibliografia:</h5>
            {api.data && <p>{api.data.bibliografia}</p>}
          </Col>
        </Row>
      </Container>
      <BotaoInfo
        funcaoAlterar={() => navigate(`/disciplina/alterar/${chave}`)}
        funcaoRemover={handleShow}
      />
      <ModalRemover
        estado={show}
        funcaoFechar={handleClose}
        funcaoRemover={RemoverDisciplina}
        entidade={"Disciplina"}
      />
    </Container>
  );
};

export default InfoDisciplina;