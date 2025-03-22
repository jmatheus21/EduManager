import React, { useEffect } from "react";
import { Col, Container, Form, Row, Alert } from "react-bootstrap";
import { useNavigate } from "react-router";
import { BotaoCadastrar, BotaoAlterar } from "../../../components";
import { useForm } from "react-hook-form";


/**
 * Componente para cadastrar ou alterar uma aula.
 * Este componente permite ao usuário cadastrar uma nova aula ou alterar os dados de uma aula existente.
 * 
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar uma aula.
 */
const Formulario = ({ enviarFormulario, alteracao }) => {
  const { register, handleSubmit, setError, reset, formState: { errors } } = useForm();
  const { alterar, dados, chave } = alteracao;
  
  const navigate = useNavigate();

  /**
   * Efeito para carregar os dados da aula quando o componente é montado ou quando o caminho da URL ou o parâmetro `chave` mudam.
   * Se o caminho da URL incluir "alterar", o título do formulário será alterado para "Alterar" e os dados da aula serão carregados.
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
   * Dependendo do caminho da URL, a função irá cadastrar uma nova aula ou alterar uma aula existente.
   * 
   * @param {Event} event - O evento de submissão do formulário.
   */
  const onSubmit = async (data) => {
 
    try {
      
      enviarFormulario(data);

    } catch (error) {
      console.error(error.message);

      if (error.message === "Aula já existe") {
        setError("id", { type: "equal" });
      }
    }
  };

  /**
   * Função para, na alteração, voltar a página de informações
   */
  const funcaoVoltar = () => navigate(`/aula/${chave}`);

  return (
        <Form className="flex-fill d-flex flex-column justify-content-between mt-4" onSubmit={handleSubmit(enviarFormulario)}>
            <Container fluid className="d-grid gap-3">
                <Row className="gap-5">
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="turmaId">Id da Turma: <span className={`${alterar? "d-none" : "" } text-danger`}>*</span></Form.Label>
                            <Form.Control
                                id="turmaId"
                                type="number"
                                className="p-2"
                                placeholder="Exemplo: 1"
                                {...register("turmaId", { required: true, valueAsNumber: true })}
                            />
                            <Alert variant="white" className={`${errors.turmaId? "" : "d-none"} text-danger`}>
                            { errors.turmaId?.type === "required" && "O id da turma é obrigatório" }
                            </Alert>
                        </Form.Group>
                    </Col>
                    <Col>
                    <Form.Group className="d-flex flex-column gap-1">
                        <Form.Label htmlFor="DisciplinaCodigo">Código da Disciplina: <span className="text-danger">*</span></Form.Label>
                        <Form.Control
                            id="DisciplinaCodigo"
                            type="text"
                            className="p-2"
                            placeholder="Exemplo: MAT001"
                            {...register("DisciplinaCodigo", { required: true, minLength: 6, maxLength: 10, pattern: /^[A-Z]{3}\d{3}$/ })}
                        />
                        <Alert variant="white" className={`${errors.DisciplinaCodigo? "" : "d-none"} text-danger`}>
                        {errors?.DisciplinaCodigo?.type == "required" && "O código da disciplina é obrigatório"}
                        {errors?.DisciplinaCodigo?.type == "minLength" && "O código da disciplina deve ter no mínimo 6 caracteres"}
                        {errors?.DisciplinaCodigo?.type == "maxLength" && "O código da disciplina deve ter no máximo 10 caracteres"}
                        {errors?.DisciplinaCodigo?.type == "pattern" && "O código da disciplina não está no formato correto. Utilize três letras maiúsculas seguidas de três números (ex: MAT123)"}
                        </Alert>
                    </Form.Group>
                    </Col>
                </Row>
                <Row className="gap-5">
                    <Col>
                    <Form.Group className="d-flex flex-column gap-1">
                        <Form.Label htmlFor="ProfessorCPF">CPF do Professor: <span className="text-danger">*</span></Form.Label>
                        <Form.Control
                            id="ProfessorCPF"
                            type="text"
                            className="p-2"
                            placeholder="Exemplo: 111.222.333-44"
                            {...register("ProfessorCPF", { required: true })}
                        />
                        <Alert variant="white" className={`${errors.ProfessorCPF? "" : "d-none"} text-danger`}>
                        {errors?.ProfessorCPF?.type == "required" && "O CPF do professor é obrigatório"}
                        </Alert>
                    </Form.Group>
                    </Col>
                </Row>
                <Row className="gap-5">
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="horaInicio">Hora de Início: <span className={`${alterar? "d-none" : "" } text-danger`}>*</span></Form.Label>
                            <Form.Control
                                id="horaInicio"
                                type="time"
                                className="p-2"
                                placeholder="Exemplo: 1"
                                {...register("horaInicio", { required: true, validate: (value) => validator.isTime(value) })}
                            />
                            <Alert variant="white" className={`${errors.horaInicio? "" : "d-none"} text-danger`}>
                            { errors.horaInicio?.type === "required" && "A hora de início é obrigatória" }
                            { errors.horaInicio?.type === "validate" && "A hora de início deve estar no formato correto" }
                            </Alert>
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="horaFim">Hora do Fim: <span className={`${alterar? "d-none" : "" } text-danger`}>*</span></Form.Label>
                            <Form.Control
                                id="horaFim"
                                type="time"
                                className="p-2"
                                placeholder="Exemplo: 1"
                                {...register("horaFim", { required: true, validate: (value) => validator.isTime(value) })}
                            />
                            <Alert variant="white" className={`${errors.horaFim? "" : "d-none"} text-danger`}>
                            { errors.horaFim?.type === "required" && "A hora do fim é obrigatória" }
                            { errors.horaFim?.type === "validate" && "A hora do fim deve estar no formato correto" }
                            </Alert>
                        </Form.Group>
                    </Col>
                </Row>
                <Row className="gap-5">
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="diasDaSemana">Dias da semana: <span className={`${alterar ? "d-none" : ""} text-danger`}>*</span></Form.Label>
                            <div id="diasDaSemana">
                                {["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"].map((dia, index) => (
                                    <Form.Check
                                        key={index}
                                        id={`${index}`}
                                        type="checkbox"
                                        label={dia}
                                        {...register(`${index}`, { required: true })}
                                    />
                                ))}
                            </div>
                            <Alert variant="white" className={`${errors.diasDaSemana ? "" : "d-none"} text-danger`}>
                                {errors.diasDaSemana?.type === "required" && "Os dias da semana são obrigatórios"}
                            </Alert>
                        </Form.Group>
                    </Col>
                </Row>
            </Container>
            {
            alterar ? <BotaoAlterar funcaoVoltar={funcaoVoltar} /> : <BotaoCadastrar />
            }
        </Form>
    );
};

export default Formulario;