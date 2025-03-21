import React, { useEffect } from "react";
import { Col, Container, Form, Row, Alert } from "react-bootstrap";
import { useNavigate } from "react-router";
import { BotaoCadastrar, BotaoAlterar } from "../../../components";
import { useForm } from "react-hook-form";


/**
 * Componente para cadastrar ou alterar uma disciplina.
 * Este componente permite ao usuário cadastrar uma nova disciplina ou alterar os dados de uma disciplina existente.
 * 
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar uma disciplina.
 */
const Formulario = ({ enviarFormulario, alteracao }) => {
  const { register, handleSubmit, setError, reset, formState: { errors } } = useForm();
  const { alterar, dados, chave } = alteracao;
  
  const navigate = useNavigate();

  /**
   * Efeito para carregar os dados da disciplina quando o componente é montado ou quando o caminho da URL ou o parâmetro `chave` mudam.
   * Se o caminho da URL incluir "alterar", o título do formulário será alterado para "Alterar" e os dados da disciplina serão carregados.
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
   * Dependendo do caminho da URL, a função irá cadastrar uma nova disciplina ou alterar uma disciplina existente.
   * 
   * @param {Event} event - O evento de submissão do formulário.
   */
  const onSubmit = async (data) => {
 
    try {
      
      enviarFormulario(data);

    } catch (error) {
      console.error(error.message);

      if (error.message === "Disciplina já existe") {
        setError("codigo", { type: "equal" });
      }
    }
  };

  /**
   * Função para, na alteração, voltar a página de informações
   */
  const funcaoVoltar = () => navigate(`/disciplina/${chave}`);

  return (
        <Form className="flex-fill d-flex flex-column justify-content-between mt-4" onSubmit={handleSubmit(onSubmit)}>
            <Container fluid className="d-grid gap-3">
                <Row className="gap-5">
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="nome">Nome: <span className="text-danger">*</span></Form.Label>
                            <Form.Control
                                id="nome"
                                type="text"
                                className="p-2"
                                placeholder="Exemplo: Matemática 1"
                                {...register("nome", { required: true, minLength: 3, maxLength: 50 })}
                            />
                        </Form.Group>
                        <Alert variant="white" className={`${errors.nome ? "" : "d-none"} text-danger`}>
                            {errors?.nome?.type == "required" && "O nome da disciplina é obrigatório"}
                            {errors?.nome?.type == "minLength" && "O nome da disciplina deve ter no mínimo 3 caracteres"}
                            {errors?.nome?.type == "maxLength" && "O nome da disciplina deve ter no máximo 50 caracteres"}
                        </Alert>
                    </Col>
                </Row>
                <Row className="gap-5">
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="codigo">Código: <span className="text-danger">*</span></Form.Label>
                            <Form.Control
                                id="codigo"
                                type="text"
                                className="p-2"
                                placeholder="Exemplo: MAT101"
                                {...register("codigo", { required: true, minLength: 6, maxLength: 10, pattern: /^[A-Z]{3}\d{3}$/ })}
                            />
                        </Form.Group>
                        <Alert variant="white" className={`${errors.codigo ? "" : "d-none"} text-danger`}>
                            {errors?.codigo?.type == "equal" && "O código da disciplina já existe"}
                            {errors?.codigo?.type == "required" && "O código da disciplina é obrigatório"}
                            {errors?.codigo?.type == "minLength" && "O código da disciplina deve ter no mínimo 6 caracteres"}
                            {errors?.codigo?.type == "maxLength" && "O código da disciplina deve ter no máximo 10 caracteres"}
                            {errors?.codigo?.type == "pattern" && "O código da disciplina não está no formato correto. Utilize três letras maiúsculas seguidas de três números (ex: MAT123)"}
                        </Alert>
                    </Col>
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="carga_horaria">Carga Horária: <span className="text-danger">*</span></Form.Label>
                            <Form.Control
                                id="carga_horaria"
                                type="number"
                                className="p-2"
                                placeholder="Exemplo: 60"
                                {...register("carga_horaria", { required: true, min: 15, max: 120, valueAsNumber: true })}
                            />
                        </Form.Group>
                        <Alert variant="white" className={`${errors.carga_horaria ? "" : "d-none"} text-danger`}>
                            {errors?.carga_horaria?.type == "required" && "A carga horária é obrigatória"}
                            {errors?.carga_horaria?.type == "min" && "A carga horária deve ser de no mínimo 15"}
                            {errors?.carga_horaria?.type == "max" && "A carga horária deve ser no máximo 120"}
                        </Alert>
                    </Col>
                </Row>
                <Row className="gap-5">
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="ementa">Ementa: </Form.Label>
                            <Form.Control
                                id="ementa"
                                type="text"
                                className="p-2"
                                placeholder="Exemplo: Álgebra, Aritmética"
                                {...register("ementa", { required: false, maxLength: 255 })}
                            />
                        </Form.Group>
                        <Alert variant="white" className={`${errors.ementa ? "" : "d-none"} text-danger`}>
                            {errors?.ementa?.type == "maxLength" && "A ementa deve ter no máximo 255 caracteres"}
                        </Alert>
                    </Col>
                </Row>
                <Row className="gap-5">
                    <Col>
                        <Form.Group className="d-flex flex-column gap-1">
                            <Form.Label htmlFor="bibliografia">Bibliografia: </Form.Label>
                            <Form.Control
                                id="bibliografia"
                                type="text"
                                className="p-2"
                                placeholder="Exemplo: Matemática 1 - Volume 1"
                                {...register("bibliografia", { required: false, maxLength: 255 })}
                            />
                        </Form.Group>
                        <Alert variant="white" className={`${errors.bibliografia ? "" : "d-none"} text-danger`}>
                            {errors?.bibliografia?.type == "maxLength" && "A bibliografia deve ter no máximo 255 caracteres"}
                        </Alert>
                    </Col>
                </Row>
                <Row>
                    <p>Os campos com <span className="text-danger">*</span> são obrigatórios.</p>
                </Row>
            </Container>
            {
                alterar ? <BotaoAlterar funcaoVoltar={funcaoVoltar} /> : <BotaoCadastrar />
            }
        </Form >
    );
};

export default Formulario;