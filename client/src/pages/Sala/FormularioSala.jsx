import React, { useEffect, useState } from "react";
import { Col, Container, Form, Row, Alert } from "react-bootstrap";
import useApi from "../../hooks/useApi";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Titulo, BotaoCadastrar, BotaoAlterar } from "../../components";
import { useForm } from "react-hook-form";

/**
 * Componente para cadastrar ou alterar uma sala.
 * Este componente permite ao usuário cadastrar uma nova sala ou alterar os dados de uma sala existente.
 * 
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar uma sala.
 */
const FormularioSala = () => {
  const { register, handleSubmit, setError, reset, formState: { errors } } = useForm();

  // Configuração padrão
  const [alterar, setAlterar] = useState(false);
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
        setAlterar(true);

        try {
          const response = await api.fetchData(`/sala/${chave}`);
          if (response) {
            reset(response);
          }
        } catch (error) {
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
   * @param data - Os dados recebidos da submissão do formulário.
   */
  const enviarFormulario = async (data) => {
 
    try {
      if (alterar) {
        if (chave != data.numero) {
          setError("numero", { type: "equal" });
          return;
        }

        await api.updateData(`/sala/${chave}`, data);

        navigate(`/sala/${data.numero}?success=true`);
      } else {
        await api.createData("/sala", data);

        navigate("/sala?success=true&type=cadastro");
      }
    } catch (error) {
      console.error(error.message);

      if (error.message === "Sala já existe") {
        setError("numero", { type: "equal" });
      }
    }
  };

  /**
   * Função para, na alteração, voltar a página de informações
   */
  const funcaoVoltar = () => navigate(`/sala/${chave}`);

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (alterar && api.loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  if (alterar && api.error) return <p>Erro: {api.error}</p>;

  return (
    <Container fluid className="d-flex flex-column">
      <Titulo>{alterar? "Alterar" : "Cadastrar"} Sala</Titulo>
      <Form className="flex-fill d-flex flex-column justify-content-between mt-4" onSubmit={handleSubmit(enviarFormulario)}>
        <Container fluid className="d-grid gap-3">
          <Row className="gap-5">
            <Col>
              <Form.Group className="d-flex flex-column gap-1">
                <Form.Label htmlFor="numero">Número: <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  id="numero"
                  type="number"
                  className="p-2"
                  {...register("numero", { required: true, min: 1, max: 1000, valueAsNumber: true })}
                />
                <Alert variant="white" className={`${errors.numero? "" : "d-none"} text-danger`}>
                  { errors.numero?.type === "equal" && "Uma sala já existe com esse número" }
                  { errors.numero?.type === "required" && "O número é obrigatório" }
                  { errors.numero?.type === "min" && "O número deve ser maior que 0" }
                  { errors.numero?.type === "max" && "O número deve ser menor que 1000" }
                </Alert>
              </Form.Group>
            </Col>
            <Col>
              <Form.Group className="d-flex flex-column gap-1">
                <Form.Label htmlFor="capacidade">Capacidade: <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  id="capacidade"
                  type="number"
                  className="p-2"
                  {...register("capacidade", { required: true, min: 10, max: 500, valueAsNumber: true })}
                />
                <Alert variant="white" className={`${errors.capacidade? "" : "d-none"} text-danger`}>
                  { errors.capacidade?.type === "required" && "A capacidade é obrigatória" }
                  { errors.capacidade?.type === "min" && "A capacidade deve ser maior que 10" }
                  { errors.capacidade?.type === "max" && "A capacidade deve ser menor que 500" }
                </Alert>
              </Form.Group>
            </Col>
          </Row>
          <Form.Group className="d-flex flex-column gap-1">
            <Form.Label htmlFor="localizacao">Localização: <span className="text-danger">*</span></Form.Label>
            <Form.Control
              id="localizacao"
              type="text"
              className="p-2"
              {...register("localizacao", { required: true, minLength: 2, maxLength: 100 })}
            />
            <Alert variant="white" className={`${errors.localizacao? "" : "d-none"} text-danger`}>
              { errors.localizacao?.type === "required" && "A localização é obrigatória" }
              { errors.localizacao?.type === "minLength" && "A localização deve ter no mínimo 2 caracteres" }
              { errors.localizacao?.type === "maxLength" && "A localização deve ter no máximo 100 caracteres" }
            </Alert>
          </Form.Group>
        </Container>
        {
          alterar ? <BotaoAlterar funcaoVoltar={funcaoVoltar} /> : <BotaoCadastrar />
        }
      </Form>
    </Container>
  );
};

export default FormularioSala;
