import React, { useEffect, useState } from "react";
import { Alert, Col, Container, Row } from "react-bootstrap";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Titulo, BotaoInfo, ModalRemover, Listagem } from "../../components";
import { inverterData, formatarCpf } from "../../components/Listagem.jsx";
import useApi from "../../hooks/useApi";

const colunas = [
  { field: "id", headerName: "#", flex: 1, align: "center", headerAlign: "center" },
  { field: "nome", headerName: "Nome", flex: 1, align: "center", headerAlign: "center" },
  { field: "salario", headerName: "Salário mensal (R$)", flex: 1, align: "center", headerAlign: "center"},
  { field: "data_contrato", headerName: "Data de contrato", flex: 1, align: "center", headerAlign: "center", valueGetter: (value, _row) => inverterData(value) },
];

/**
 * Componente para exibir informações detalhadas de um usuário.
 * Este componente permite visualizar os detalhes de um usuário específico, além de oferecer opções para alterar ou remover o usuário.
 *
 * @returns {JSX.Element} O componente de informações do usuário.
 */
const InfoUsuario = () => {
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
   * Função para remover o usuário.
   * Após a remoção bem-sucedida, o usuário é redirecionado para a lista de usuários.
   */
  const RemoverUsuario = async () => {
    try {
      await api.deleteData(`/usuario/${chave}`);
      navigate("/usuario?success=true&type=remocao");
    } catch (error) {
      console.error("Erro ao remover usuário:", error);
      alert("Erro ao remover usuário, tente novamente mais tarde");
    }
  };

  /**
   * Efeito para buscar os dados do usuário ao carregar o componente ou quando o cpf do usuário muda.
   */
  useEffect(() => {
    api.fetchData(`/usuario/${chave}`);
  }, [chave]);

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (api.loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  if (api.error) return <p>Erro: {api.error}</p>;

  const exibirDisciplinas = (disciplinas) => {
    return disciplinas.map((item, index) => {
      if (disciplinas.length == 1) {
        return (<span key={index}>{item.nome} ({item.codigo})</span>)
      } else if ((disciplinas.length - 1) == index) {
        return (<span key={index}> e {item.nome} ({item.codigo})</span>)
      } else {
        return (<span key={index}>{item.nome} ({item.codigo},)</span>)
      }
    })
  }

  return (
    <Container fluid className="d-flex flex-column justify-content-between">
      <Titulo>Informações do Usuário</Titulo>
      {successParam && (
        <Alert variant="success" className="p-3 mt-3">
          Usuário alterado com sucesso!
        </Alert>
      )}
      <Container fluid className="my-4 d-grid gap-3">
        <Row>
          <Col>
            <h5>Nome:</h5>
            {api.data && <p>{api.data.nome}</p>}
          </Col>
          <Col>
            <h5>Tipo:</h5>
            {api.data && <p>{api.data.tipo == "p" ? "Professor" : "Funcionário"}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>CPF:</h5>
            {api.data && <p>{formatarCpf(api.data.cpf)}</p>}
          </Col>
          <Col>
            <h5>E-mail:</h5>
            {api.data && <p>{api.data.email}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Horário de Trabalho:</h5>
            {api.data && <p>{api.data.horario_de_trabalho}</p>}
          </Col>
          <Col>
            <h5>Telefone:</h5>
            {api.data && <p>{api.data.telefone}</p>}
          </Col>
          <Col>
            <h5>Data de nascimento:</h5>
            {api.data && <p>{inverterData(api.data.data_de_nascimento)}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Endereço:</h5>
            {api.data && <p>{api.data.endereco}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Formação:</h5>
            {api.data && <p>{api.data.formacao}</p>}
          </Col>
        </Row>
        <Row>
          <Col>
            <h5>Cargos:</h5>
          </Col>
        </Row>
        {api.data && <Listagem colunas={colunas} data={api.data.cargos} pk={colunas[0].field} />}
        <Row>
          <Col>
            <h5>Disciplinas:</h5>
            <p>
              {api.data && exibirDisciplinas(api.data.disciplinas)}
            </p>
          </Col>
        </Row>
      </Container>
      <BotaoInfo
        funcaoAlterar={() => navigate(`/usuario/alterar/${chave}`)}
        funcaoRemover={handleShow}
      />
      <ModalRemover
        estado={show}
        funcaoFechar={handleClose}
        funcaoRemover={RemoverUsuario}
        entidade={"Usuario"}
      />
    </Container>
  );
};

export default InfoUsuario;
