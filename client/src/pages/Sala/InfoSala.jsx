import React, { useEffect, useState } from "react";
import { Alert, Col, Container, Row } from "react-bootstrap";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Titulo, BotaoInfo, ModalRemover } from "../../components";
import useApi from "../../hooks/useApi";

/**
 * Componente para exibir informações detalhadas de uma sala.
 * Este componente permite visualizar os detalhes de uma sala específica, além de oferecer opções para alterar ou remover a sala.
 *
 * @returns {JSX.Element} O componente de informações da sala.
 */
const InfoSala = () => {
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
   * Função para remover a sala.
   * Após a remoção bem-sucedida, o usuário é redirecionado para a lista de salas.
   */
  const RemoverSala = async () => {
    try {
      await api.deleteData(`/sala/${chave}`);
      navigate("/sala?success=true&type=remocao");
    } catch (error) {
      console.error("Erro ao remover sala:", error);
      alert("Erro ao remover sala, tente novamente mais tarde");
    }
  };

  /**
   * Efeito para buscar os dados da sala ao carregar o componente ou quando o número da sala muda.
   */
  useEffect(() => {
    api.fetchData(`/sala/${chave}`);
  }, [chave]);

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (api.loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  if (api.error) return <p>Erro: {api.error}</p>;

  return (
    <Container fluid className="d-flex flex-column justify-content-between">
      <Titulo>Informações da Sala</Titulo>
      {successParam && (
        <Alert variant="success" className="p-3 mt-3">
          Sala alterada com sucesso!
        </Alert>
      )}
      <Container fluid className="my-4 d-grid gap-3">
        <Row>
          <Col>
            <h5>Número:</h5>
            {api.data && <p>{api.data.numero}</p>}
          </Col>
          <Col>
            <h5>Capacidade:</h5>
            {api.data && <p>{api.data.capacidade}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Localização:</h5>
            {api.data && <p>{api.data.localizacao}</p>}
          </Col>
        </Row>
      </Container>
      <BotaoInfo
        funcaoAlterar={() => navigate(`/sala/alterar/${chave}`)}
        funcaoRemover={handleShow}
      />
      <ModalRemover
        estado={show}
        funcaoFechar={handleClose}
        funcaoRemover={RemoverSala}
        entidade={"Sala"}
      />
    </Container>
  );
};

export default InfoSala;
