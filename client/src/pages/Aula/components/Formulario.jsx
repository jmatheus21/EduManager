import React, { useEffect } from "react";
import { Col, Container, Form, Row, Alert } from "react-bootstrap";
import { useNavigate } from "react-router";
import { BotaoCadastrar, BotaoAlterar } from "../../../components";
import { Controller, useForm } from "react-hook-form";
import validator from "validator";
import { IMaskInput } from "react-imask";


/**
 * Componente para cadastrar ou alterar uma aula.
 * Este componente permite ao usuário cadastrar uma nova aula ou alterar os dados de uma aula existente.
 * 
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar uma aula.
 */
const Formulario = ({ enviarFormulario, alteracao }) => {
    const { register, handleSubmit, control, setError, reset, formState: { errors } } = useForm();
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

            await enviarFormulario(data);

        } catch (error) {
            console.error(error.message);

            if (error.message === "Aula já existe") {
                setError("id", { type: "equal" });
            }

            if (error.message.includes("Turma não existe")) {
                setError("root.serverError", { message: "A turma não existe" });
            }

            if (error.message.includes("O usuário não é do tipo 'professor'")) {
                setError("root.serverError", { message: "Apenas professores podem realizar esta ação." });
            }
        }
    };

    /**
     * Função para, na alteração, voltar a página de informações
     */
    const funcaoVoltar = () => navigate(`/aula/${chave}`);

    return (
        <Form className="flex-fill d-flex flex-column justify-content-between mt-4" onSubmit={handleSubmit(onSubmit)}>
            <Container fluid className="d-grid gap-3">
                <Row className="gap-5">
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="turmaId">Id da Turma: <span className={`${alterar ? "d-none" : ""} text-danger`}>*</span></Form.Label>
                            <Form.Control
                                id="turmaId"
                                type="number"
                                className="p-2"
                                placeholder="Exemplo: 1"
                                {...register("turma_id", { required: true, valueAsNumber: true })}
                            />
                            <Alert variant="white" className={`${errors.turma_id ? "" : "d-none"} text-danger`}>
                                {errors.turma_id?.type === "required" && "O id da turma é obrigatório"}
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
                                {...register("disciplina_codigo", { required: true, minLength: 6, maxLength: 10, pattern: /^[A-Z]{3}\d{3}$/ })}
                            />
                            <Alert variant="white" className={`${errors.disciplina_codigo ? "" : "d-none"} text-danger`}>
                                {errors?.disciplina_codigo?.type == "required" && "O código da disciplina é obrigatório"}
                                {errors?.disciplina_codigo?.type == "minLength" && "O código da disciplina deve ter no mínimo 6 caracteres"}
                                {errors?.disciplina_codigo?.type == "maxLength" && "O código da disciplina deve ter no máximo 10 caracteres"}
                                {errors?.disciplina_codigo?.type == "pattern" && "O código da disciplina não está no formato correto. Utilize três letras maiúsculas seguidas de três números (ex: MAT123)"}
                            </Alert>
                        </Form.Group>
                    </Col>
                </Row>
                <Row className="gap-5">
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="usuario_cpf">CPF do Professor: <span className="text-danger">*</span></Form.Label>
                            <Controller
                                name="usuario_cpf"
                                control={control}
                                defaultValue=""
                                rules={{ required: !alterar }}
                                render={({ field }) => (
                                <IMaskInput
                                    {...field}
                                    id="usuario_cpf"
                                    mask="000.000.000-00"
                                    placeholder="Exemplo: 999.888.777-66"
                                    className="p-2 form-control"
                                />
                                )}
                            />
                            <Alert variant="white" className={`${errors.usuario_cpf ? "" : "d-none"} text-danger`}>
                                {errors?.usuario_cpf?.type == "required" && "O CPF do professor é obrigatório"}
                            </Alert>
                        </Form.Group>
                    </Col>
                </Row>
                <Row className="gap-5">
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="horaInicio">Hora de Início: <span className={`${alterar ? "d-none" : ""} text-danger`}>*</span></Form.Label>
                            <Form.Control
                                id="horaInicio"
                                type="time"
                                className="p-2"
                                placeholder="Exemplo: 1"
                                {...register("hora_inicio", { required: true, validate: (value) => validator.isTime(value) })}
                            />
                            <Alert variant="white" className={`${errors.hora_inicio ? "" : "d-none"} text-danger`}>
                                {errors.hora_inicio?.type === "required" && "A hora de início é obrigatória"}
                                {errors.hora_inicio?.type === "validate" && "A hora de início deve estar no formato correto"}
                            </Alert>
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="horaFim">Hora do Fim: <span className={`${alterar ? "d-none" : ""} text-danger`}>*</span></Form.Label>
                            <Form.Control
                                id="horaFim"
                                type="time"
                                className="p-2"
                                placeholder="Exemplo: 1"
                                {...register("hora_fim", { required: true, validate: (value) => validator.isTime(value) })}
                            />
                            <Alert variant="white" className={`${errors.hora_fim ? "" : "d-none"} text-danger`}>
                                {errors.hora_fim?.type === "required" && "A hora do fim é obrigatória"}
                                {errors.hora_fim?.type === "validate" && "A hora do fim deve estar no formato correto"}
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
                                        id={`diasDaSemana-${index}`}
                                        type="checkbox"
                                        label={dia}
                                        value={dia}
                                        {...register("dias_da_semana", {
                                            required: { value: true, message: "Os dias da semana são obrigatórios" }
                                        })}
                                    />
                                ))}
                            </div>
                            <Alert variant="white" className={`${errors.dias_da_semana ? "" : "d-none"} text-danger`}>
                                {errors.dias_da_semana?.message}
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