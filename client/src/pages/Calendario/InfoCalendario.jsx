import React, { useEffect, useState } from "react";
import { Alert, Col, Container, Row } from "react-bootstrap";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Titulo, BotaoInfo, ModalRemover } from "../../components";
import useApi from "../../hooks/useApi";
import { inverterData } from "../../components/Listagem.jsx"; 

/**
 * Componente para exibir informações detalhadas de um calendário.
 * Este componente permite visualizar os detalhes de um calendário específico, além de oferecer opções para alterar ou remover o calendário.
 *
 * @returns {JSX.Element} O componente de informações do calendário.
 */
const InfoCalendario = () => {
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
   * Função para remover o calendário.
   * Após a remoção bem-sucedida, o usuário é redirecionado para a lista de calendários.
   */
  const RemoverCalendario = async () => {
    try {
      await api.deleteData(`/calendario/${chave}`);
      navigate("/calendario?success=true&type=remocao");
    } catch (error) {
      console.error("Erro ao remover calendário:", error);
      alert("Erro ao remover calendário, tente novamente mais tarde");
    }
  };

  /**
   * Efeito para buscar os dados do calendário ao carregar o componente ou quando o ano letivo do calendário muda.
   */
  useEffect(() => {
    api.fetchData(`/calendario/${chave}`);
  }, [chave]);

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (api.loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  if (api.error) return <p>Erro: {api.error}</p>;

  return (
    <Container fluid className="d-flex flex-column justify-content-between">
      <Titulo>Informações do Calendário</Titulo>
      {successParam && (
        <Alert variant="success" className="p-3 mt-3">
          Calendário alterado com sucesso!
        </Alert>
      )}
      <Container fluid className="my-4 d-grid gap-3">
        <Row>
          <Col>
            <h5>Ano Letivo:</h5>
            {api.data && <p data-testid="chave_primaria">{api.data.ano_letivo}</p>}
          </Col>
          <Col>
            <h5>Dias letivos:</h5>
            {api.data && <p>{api.data.dias_letivos}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Data de início:</h5>
            {api.data && <p>{inverterData(api.data.data_inicio)}</p>}
          </Col>
          <Col>
            <h5>Data de fim:</h5>
            {api.data && <p>{inverterData(api.data.data_fim)}</p>}
          </Col>
        </Row>
      </Container>
      <BotaoInfo
        funcaoAlterar={() => navigate(`/calendario/alterar/${chave}`)}
        funcaoRemover={handleShow}
      />
      <ModalRemover
        estado={show}
        funcaoFechar={handleClose}
        funcaoRemover={RemoverCalendario}
        entidade={"Calendário"}
      />
    </Container>
  );
};

export default InfoCalendario;
