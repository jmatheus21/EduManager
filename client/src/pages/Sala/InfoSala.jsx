import React, { useEffect, useState } from "react";
import { Col, Container, Row } from "react-bootstrap";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Titulo, BotaoInfo, ModalRemover } from "../../components";
import ModalRemoverSalaErro from "./components/ModalRemoverSala";
import useApi from "../../hooks/useApi";
import { Alert } from "@mui/material";

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
  const [showError, setShowError] = useState(false);
  const { deleteData, fetchData, loading, data } = useApi("/api");

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
      await deleteData(`/sala/${chave}`);
      navigate("/sala?success=true&type=remocao");
    } catch (error) {
      if (error.message.includes("Não é possível remover a sala, pois há turmas ativas associadas a essa sala")) {
        handleClose();
        setShowError(true);
      } else {
        alert("Erro ao remover sala, tente novamente mais tarde");
      }
    }
  };

  /**
   * Efeito para buscar os dados da sala ao carregar o componente ou quando o número da sala muda.
   */
  useEffect(() => {
    fetchData(`/sala/${chave}`);
  }, [chave]);

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  // if (error) return <p>Erro: {error}</p>;

  return (
    <Container fluid className="d-flex flex-column justify-content-between">
      <Titulo>Informações da Sala</Titulo>
      {successParam && (
        <Alert severity="success" className="p-3 mt-3 d-flex align-content-center gap-3">
          Sala alterada com sucesso!
        </Alert>
      )}
      <Container fluid className="my-4 d-grid gap-3">
        <Row>
          <Col>
            <h5>Número:</h5>
            {data && <p>{data.numero}</p>}
          </Col>
          <Col>
            <h5>Capacidade:</h5>
            {data && <p>{data.capacidade}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Localização:</h5>
            {data && <p>{data.localizacao}</p>}
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
      <ModalRemoverSalaErro 
        estado={showError}
        funcaoFechar={() => setShowError(false)}
      />
    </Container>
  );
};

export default InfoSala;
