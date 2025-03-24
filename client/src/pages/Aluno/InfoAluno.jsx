import React, { useEffect, useState } from "react";
import { Alert, Col, Container, Row } from "react-bootstrap";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Titulo, BotaoInfo, ModalRemover } from "../../components";
import useApi from "../../hooks/useApi";

/**
 * Componente para exibir informações detalhadas de um Aluno.
 * Este componente permite visualizar os detalhes de um aluno específico, além de oferecer opções para alterar ou remover a aluno.
 *
 * @returns {JSX.Element} O componente de informações do aluno.
 */
const InfoAluno = () => {
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
   * Função para remover o aluno.
   * Após a remoção bem-sucedida, o usuário é redirecionado para a lista de alunos.
   */
  const RemoverAluno= async () => {
    try {
      await api.deleteData(`/aluno/${chave}`);
      navigate("/aluno?success=true&type=remocao");
    } catch (error) {
      console.error("Erro ao remover aluno:", error);
      alert("Erro ao remover aluno, tente novamente mais tarde");
    }
  };

  /**
   * Efeito para buscar os dados do aluno ao carregar o componente.
   */
  useEffect(() => {
    api.fetchData(`/aluno/${chave}`);
  }, [chave]);

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (api.loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  if (api.error) return <p>Erro: {api.error}</p>;

  const exibirTurma = (turmas) => {
    var i, turma, maior_ano = 0;
    for (i = 0; i < turmas.length - 1; i++) {
        if (turmas[i].ano > maior_ano) {
            maior_ano = turmas[i].ano;
            turma = turma[i];
        }
    }

    return (<span key={i}>{turma.ano} ano {turma.serie} - {turma.nivel_de_ensino} ({turma.id}), </span>)
  }

  return (
    <Container fluid className="d-flex flex-column justify-content-between">
      <Titulo>Informações do Aluno</Titulo>
      {successParam && (
        <Alert variant="success" className="p-3 mt-3">
          Aluno alterado com sucesso!
        </Alert>
      )}
      <Container fluid className="my-4 d-grid gap-3">
        <Row>
          <Col>
            <h5>Matrícula:</h5>
            {api.data && <p data-testid="chave_primaria">{api.data.matricula}</p>}
          </Col>
          <Col>
            <h5>Turma:</h5>
            {api.data && <p data-testid="turma_id">{api.data.turma_id}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Nome:</h5>
            {api.data && <p>{api.data.nome}</p>}
          </Col>
          <Col>
            <h5>Email:</h5>
            {api.data && <p>{api.data.email}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Telefone:</h5>
            {api.data && <p>{api.data.telefone}</p>}
          </Col>
          <Col>
            <h5>Data de Nascimento:</h5>
            {api.data && <p>{api.data.data_de_nascimento}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Endereço:</h5>
            {api.data && <p>{api.data.endereco}</p>}
          </Col>
        </Row>
      </Container>
      <BotaoInfo
        funcaoAlterar={() => navigate(`/aluno/alterar/${chave}`)}
        funcaoRemover={handleShow}
      />
      <ModalRemover
        estado={show}
        funcaoFechar={handleClose}
        funcaoRemover={RemoverAluno}
        entidade={"Aluno"}
      />
    </Container>
  );
};

export default InfoAluno;