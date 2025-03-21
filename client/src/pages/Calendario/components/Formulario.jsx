import React, { useEffect } from "react";
import { Col, Form, Row, Alert, Container } from "react-bootstrap";
import { useNavigate } from "react-router";
import { BotaoCadastrar, BotaoAlterar } from "../../../components";
import { useForm } from "react-hook-form";
import validator from "validator";

const anoAtual = new Date().getFullYear();

/**
 * Componente para cadastrar ou alterar um calendário.
 * Este componente permite ao usuário cadastrar um novo calendário ou alterar os dados de um calendário existente.
 * 
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar um calendário.
 */
const Formulario = ({ enviarFormulario, alteracao }) => {
  const { register, handleSubmit, watch, setError, reset, formState: { errors } } = useForm();
  const { alterar, dados, chave } = alteracao;
  const dataInicio = watch("data_inicio");
  const anoLetivo = watch("ano_letivo");
  const navigate = useNavigate();

  /**
   * Efeito para carregar os dados do calendário quando o componente é montado ou quando o caminho da URL ou o parâmetro `chave` mudam.
   * Se o caminho da URL incluir "alterar", o título do formulário será alterado para "Alterar" e os dados do calendário serão carregados.
   */
  useEffect(() => {
    const carregarDados = async () => {
      if (alterar && dados) {
        reset(dados)
      }
    };

    carregarDados();
  }, [alterar, dados, reset]);

  /**
   * Função para lidar com o envio do formulário.
   * Dependendo do caminho da URL, a função irá cadastrar um novo calendário ou alterar um calenário existente.
   * 
   * @param {Event} event - O evento de submissão do formulário.
   */
  const onSubmit = async (data) => {
 
    try {
      
      enviarFormulario(data);

    } catch (error) {
      console.error(error.message);

      if (error.message === "Calendário já existe") {
        setError("ano_letivo", { type: "equal" });
      }
    }
  };

  /**
   * Função para, na alteração, voltar a página de informações
   */
  const funcaoVoltar = () => navigate(`/calendario/${chave}`);

  return (
      <Form className="flex-fill d-flex flex-column justify-content-between mt-4" onSubmit={handleSubmit(enviarFormulario)}>
        <Container fluid className="d-grid gap-3">
          <Row className="gap-5">
            <Col>
              <Form.Group className="d-flex flex-column gap-1">
                <Form.Label htmlFor="anoLetivo">Ano letivo: <span className={`${alterar? "d-none" : ""} text-danger`}>*</span></Form.Label>
                <Form.Control
                  id="anoLetivo"
                  disabled={alterar}
                  type="number"
                  className="p-2"
                  placeholder="Exemplo: 2026"
                  {...register("ano_letivo", { required: !alterar, validate: (value) => value >= anoAtual, valueAsNumber: true })}
                />
                <Alert variant="white" className={`${errors.ano_letivo? "" : "d-none"} text-danger`}>
                    {errors?.ano_letivo?.type == "equal" && "O calendário já existe"}
                    {errors?.ano_letivo?.type == "required" && "O ano letivo é obrigatório"}
                    {errors?.ano_letivo?.type == "validate" && `O ano deve ser igual ou maior que ${anoAtual}`}
                </Alert>
              </Form.Group>
            </Col>
            <Col>
              <Form.Group className="d-flex flex-column gap-1">
                <Form.Label htmlFor="diasLetivos">Dias letivos: <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  id="diasLetivos"
                  type="number"
                  className="p-2"
                  placeholder="Exemplo: 150"
                  {...register("dias_letivos", { required: true, min: 50, max: 200, valueAsNumber: true })}
                />
                <Alert variant="white" className={`${errors.dias_letivos? "" : "d-none"} text-danger`}>
                    {errors?.dias_letivos?.type == "required" && "A quantidade de dias letivos é obrigatória"}
                    {errors?.dias_letivos?.type == "min" && "A quantidade de dias letivos deve ser no mínimo 50"}
                    {errors?.dias_letivos?.type == "max" && "A quantidade de dias letivos deve ser no máximo 200"}
                </Alert>
              </Form.Group>
            </Col>
          </Row>
          <Row className="gap-5">
            <Col>
              <Form.Group className="d-flex flex-column gap-1">
                <Form.Label htmlFor="data_inicio">Data de início: <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  id="data_inicio"
                  type="date"
                  className="p-2"
                  {...register("data_inicio", { required: true, validate: (value) => validator.isDate(value) && anoLetivo == value.slice(0, 4) })}
                />
                <Alert variant="white" className={`${errors.data_inicio? "" : "d-none"} text-danger`}>
                    {errors?.data_inicio?.type == "required" && "A data de início é obrigatória"}
                    {errors?.data_inicio?.type == "validate" && "A data de início deve ser no mesmo ano letivo inserido"}
                </Alert>
              </Form.Group>
            </Col>
            <Col>
              <Form.Group className="d-flex flex-column gap-1">
              <Form.Label htmlFor="data_fim">Data de fim: <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  id="data_fim"
                  type="date"
                  className="p-2"
                  {...register("data_fim", { required: true, validate: (value) => validator.isDate(value) && validator.isAfter(value, dataInicio) && anoLetivo == value.slice(0, 4)})}
                />
                <Alert variant="white" className={`${errors.data_fim? "" : "d-none"} text-danger`}>
                    {errors?.data_fim?.type == "required" && "A data de fim é obrigatória"}
                    {errors?.data_fim?.type == "validate" && "A data de fim é anterior à data de início ou ela não pertence ao mesmo ano letivo"}
                </Alert>
              </Form.Group>
            </Col>
          </Row>
          <Row>
              <p>Os campos com <span className="text-danger">*</span> são obrigatórios.</p>
          </Row>
        </Container>
        {
          alterar? <BotaoAlterar funcaoVoltar={funcaoVoltar} /> : <BotaoCadastrar />
        }
      </Form>
  );
};

export default Formulario;