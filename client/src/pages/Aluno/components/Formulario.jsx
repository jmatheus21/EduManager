import React, { useEffect } from "react";
import { Col, Container, Form, Row, Alert } from "react-bootstrap";
import { useNavigate } from "react-router";
import { BotaoCadastrar, BotaoAlterar } from "../../../components";
import { useForm, Controller } from "react-hook-form";
import { IMaskInput } from "react-imask";
import { isDate, isEmail, isBefore, isAfter } from "validator";


const anoAtual = new Date().getFullYear();
const maxData = `${anoAtual - 6}-12-31`;
const minData = `${anoAtual - 100}-01-01`;


/**
 * Componente para cadastrar ou alterar um aluno.
 * Este componente permite ao usuário cadastrar um novo aluno ou alterar os dados de um aluno existente.
 * 
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar um aluno.
 */
const Formulario = ({ enviarFormulario, alteracao }) => {
  const { control, register, handleSubmit, setError, reset, formState: { errors } } = useForm();
  const { alterar, dados, chave } = alteracao;
  
  const navigate = useNavigate();

  /**
   * Efeito para carregar os dados do aluno quando o componente é montado ou quando o caminho da URL ou o parâmetro `chave` mudam.
   * Se o caminho da URL incluir "alterar", o título do formulário será alterado para "Alterar" e os dados do aluno serão carregados.
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
   * Dependendo do caminho da URL, a função irá cadastrar um novo aluno ou alterar um aluno existente.
   * 
   * @param {Event} event - O evento de submissão do formulário.
   */
  const onSubmit = async (data) => {
 
    try {
      
      enviarFormulario(data);

    } catch (error) {
      console.error(error.message);

      if (error.message === "Aluno já existe") {
        setError("matricula", { type: "equal" });
      }

      if (error.message === "E-mail já existe") {
        setError("email", { type: "equal" });
      }

      if (error.message === "A turma está fechada, portanto, não é possível cadastrar mais alunos") {
        setError("idTurma", { type: "void" });
      }

    }
  };

  /**
   * Função para, na alteração, voltar a página de informações
   */
  const funcaoVoltar = () => navigate(`/aluno/${chave}`);

  return (
        <Form className="flex-fill d-flex flex-column justify-content-between mt-4" onSubmit={handleSubmit(onSubmit)}>
            <Container fluid className="d-grid gap-3">
            <Row className="gap-5">
                <Col>
                <Form.Group className="d-flex flex-column gap-1">
                    <Form.Label htmlFor="nome">Aluno: <span className={`${alterar? "d-none" : "" } text-danger`}>*</span></Form.Label>
                    <Form.Control
                    id="nome"
                    type="text"
                    className="p-2"
                    placeholder="Exemplo: João Paulo Silva"
                    {...register("nome", { required: true, minLength: 3, maxLength: 100 })}
                    />
                    <Alert variant="white" className={`${errors.nome? "" : "d-none"} text-danger`}>
                    { errors.nome?.type === "required" && "O nome é obrigatório" }
                    { errors.nome?.type === "minLength" && "O nome deve ter no minímo 3 caracteres" }
                    { errors.nome?.type === "maxLength" && "O nome deve ter no máximo 100 caracteres" }
                    </Alert>
                </Form.Group>
                </Col>
            </Row>
            <Row className="gap-5">
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="email">Email: <span className={`${alterar? "d-none" : "" } text-danger`}>*</span></Form.Label>
                  <Form.Control
                    id="email"
                    type="text"
                    className="p-2"
                    placeholder="Exemplo: jpsilva@terra.com.br"
                    {...register('email', { required: true, minLength: 3, maxLength: 100,  validate: (value) => isEmail(value)})}
                  />
                  <Alert variant="white" className={`${errors.email? "" : "d-none"} text-danger`}>
                    {errors?.email?.type == "required" && "O e-mail é obrigatório"}
                    {errors?.email?.type == "equal" && "O e-mail pertence a outro usuário"}
                    {errors?.email?.type == "minLength" && "O e-mail deve ter no mínimo 3 caracteres"}
                    {errors?.email?.type == "maxLength" && "O e-mail deve ter no máximo 100 caracteres"}
                    {errors?.email?.type == "validate" && "O e-mail está no formato errado ou não é um e-mail válido"}
                  </Alert>
                </Form.Group>
              </Col>
            </Row>
            <Row className="gap-5">
                <Col>
                    <Form.Group className="d-flex flex-column gap-1">
                    <Form.Label htmlFor="telefone">Telefone: <span className="text-danger">*</span></Form.Label>
                    <Controller
                        name="telefone"
                        control={control}
                        defaultValue=""
                        rules={{ required: true }}
                        render={({ field }) => (
                        <IMaskInput
                            {...field}
                            id="telefone"
                            mask="00 9 0000-0000"
                            placeholder="Exemplo: 99 9 8887-7766"
                            className="p-2 form-control"
                        />
                        )}
                    />
                    <Alert variant="white" className={`${errors.telefone? "" : "d-none"} text-danger`}>
                        {errors?.telefone?.type == "required" && "O telefone é obrigatório"}
                        {errors?.telefone?.type == "maxLength" && "O telefone deve ter no máximo 50 caracteres"}
                    </Alert>
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="d-flex flex-column gap-1">
                    <Form.Label htmlFor="dataNascimento">Data de Nascimento: <span className="text-danger">*</span></Form.Label>
                    <Form.Control
                        id="dataNascimento"
                        type="date"
                        className="p-2"
                        {...register('data_de_nascimento', { required: true, validate: (value) => isDate(value) && isBefore(value, maxData) && isAfter(value, minData) })}
                    />
                    <Alert variant="white" className={`${errors.data_de_nascimento? "" : "d-none"} text-danger`}>
                        {errors?.data_de_nascimento?.type == "required" && "A data de nascimento é obrigatória"}
                        {errors?.data_de_nascimento?.type == "validate" && "O usuário deve ter entre 6 e 100 anos"}
                    </Alert>
                    </Form.Group>
                </Col>
            </Row>
            <Row className="gap-5">
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="endereco">Endereço: <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    id="endereco"
                    as="textarea"
                    style={{ resize: 'none' }}
                    className="p-2"
                    placeholder="Exemplo: Rua das Flores, N° 24, Bairro Industrial, Carira/SE"
                    {...register('endereco', { required: true, minLength: 10, maxLength: 255 })}
                  />
                  <Alert variant="white" className={`${errors.endereco? "" : "d-none"} text-danger`}>
                    {errors?.endereco?.type == "required" && "O endereço é obrigatório"}
                    {errors?.endereco?.type == "minLength" && "O endereço deve ter no mímimo 10 caracteres"}
                    {errors?.endereco?.type == "maxLength" && "O endereço deve ter no máximo 255 caracteres"}
                  </Alert>
                </Form.Group>
              </Col>
            </Row>
            <Row className="gap-5">
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="idTurma">Id da Turma: <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    id="idTurma"
                    type="number"
                    className="p-2"
                    placeholder="Exemplo: 1"
                    {...register("turma_id", { required: true, valueAsNumber: true })}
                  />
                  <Alert variant="white" className={`${errors.turma_id? "" : "d-none"} text-danger`}>
                      {errors?.turma_id?.type == "required" && "O id da turma é obrigatório"}
                      {errors?.turma_id?.type == "void" && "A turma está consolidada, ou seja, não é possível matricular o aluno"}
                  </Alert>
                </Form.Group>
              </Col>
            </Row>
            <Row>
                <p>Os campos com <span className="text-danger">*</span> são obrigatórios.</p>
            </Row>
            </Container>
            {
            alterar ? <BotaoAlterar funcaoVoltar={funcaoVoltar} /> : <BotaoCadastrar />
            }
        </Form>
    );
};

export default Formulario;