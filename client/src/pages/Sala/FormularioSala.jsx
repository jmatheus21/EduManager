import React, { useEffect, useState } from "react";
import { Col, Container, Form, Row, Alert } from "react-bootstrap";
import useApi from "../../hooks/useApi";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Titulo, BotaoCadastrar, BotaoAlterar } from "../../components";

/**
 * Componente para cadastrar ou alterar uma sala.
 * Este componente permite ao usuário cadastrar uma nova sala ou alterar os dados de uma sala existente.
 * 
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar uma sala.
 */
const FormularioSala = () => {
  // Configuração dos atributos
  const [numero, setNumero] = useState(0);
  const [capacidade, setCapacidade] = useState(0);
  const [localizacao, setLocalizacao] = useState("");

  // Configuração padrão
  const [titulo, setTitulo] = useState("Cadastrar");
  const [erros, setErros] = useState([]);
  const api = useApi("/api");
  const navigate = useNavigate();
  const url = useLocation();
  const { chave } = useParams();

  /**
   * Efeito para carregar os dados da sala quando o componente é montado ou quando o caminho da URL ou o parâmetro `chave` mudam.
   * Se o caminho da URL incluir "alterar", o título do formulário será alterado para "Alterar" e os dados da sala serão carregados.
   */
  useEffect(() => {
    const carregarDados = async () => {
      if (url.pathname.includes("alterar")) {
        setTitulo("Alterar");

        try {
          const response = await api.fetchData(`/sala/${chave}`);
          if (response) {
            setNumero(response.numero);
            setCapacidade(response.capacidade);
            setLocalizacao(response.localizacao);
          }
        } catch (error) {
          setTextAlert(error);
          console.error("Erro ao carregar dados da sala:", error);
        }
      }
    };

    carregarDados();
  }, [url.pathname, chave]);

  /**
   * Função para lidar com o envio do formulário.
   * Dependendo do caminho da URL, a função irá cadastrar uma nova sala ou alterar uma sala existente.
   * 
   * @param {Event} event - O evento de submissão do formulário.
   */
  const enviarFormulario = async (event) => {
    event.preventDefault();

    const nova_sala = {
      numero: numero,
      capacidade: capacidade,
      localizacao: localizacao,
    };

    try {
      if (location.pathname.includes("alterar")) {
        await api.updateData(`/sala/${chave}`, nova_sala);

        navigate(`/sala/${numero}?success=true`);
      } else {
        await api.createData("/sala", nova_sala);

        navigate("/sala?success=true&type=cadastro");
      }
    } catch (error) {
      console.error(error.message);

      if (typeof (error.message) == "string") {
        setErros(error.message.split(","));
      }
    }
  };

  /**
   * Função para, na alteração, voltar a página de informações
   */
  const funcaoVoltar = () => navigate(`/sala/${numero}`);

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (titulo.includes("Alterar") && api.loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  if (titulo.includes("Alterar") && api.error) return <p>Erro: {api.error}</p>;

  return (
    <Container fluid className="d-flex flex-column">
      <Titulo>{titulo} Sala</Titulo>
      {
        erros?.map((erro, index) => (
          <Alert key={index} variant="danger" className="p-3 my-3">
            {erro}
          </Alert>
        ))
      }
      <Form className="flex-fill d-flex flex-column justify-content-between mt-4" onSubmit={enviarFormulario}>
        <Container className="d-grid gap-3">
          <Row className="gap-5">
            <Col>
              <Form.Group className="d-flex flex-column gap-1">
                <Form.Label htmlFor="numero">Número:</Form.Label>
                <Form.Control
                  id="numero"
                  type="number"
                  className="p-2"
                  value={numero}
                  min={1}
                  onChange={(event) => setNumero(Number(event.target.value))}
                />
              </Form.Group>
            </Col>
            <Col>
              <Form.Group className="d-flex flex-column gap-1">
                <Form.Label htmlFor="capacidade">Capacidade:</Form.Label>
                <Form.Control
                  id="capacidade"
                  type="number"
                  className="p-2"
                  value={capacidade}
                  min={10}
                  onChange={(event) => setCapacidade(Number(event.target.value))}
                />
              </Form.Group>
            </Col>
          </Row>
          <Form.Group className="d-flex flex-column gap-1">
            <Form.Label htmlFor="localizacao">Localização:</Form.Label>
            <Form.Control
              id="localizacao"
              type="text"
              className="p-2"
              value={localizacao}
              maxLength={100}
              onChange={(event) => setLocalizacao(event.target.value)}
            />
          </Form.Group>
        </Container>
        {
          titulo.includes("Alterar") ? <BotaoAlterar funcaoVoltar={funcaoVoltar} /> : <BotaoCadastrar />
        }
      </Form>
    </Container>
  );
};

export default FormularioSala;
