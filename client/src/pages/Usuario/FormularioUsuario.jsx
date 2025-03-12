import React, { useEffect, useState } from "react";
import { Col, Container, Form, Row, Alert } from "react-bootstrap";
import useApi from "../../hooks/useApi";
import { IMaskInput } from "react-imask";
import { useLocation, useNavigate, useParams } from "react-router";
import { Titulo, BotaoCadastrar, BotaoAlterar } from "../../components";
import { useForm, Controller, useFieldArray } from "react-hook-form";
import { isDate, isEmail, isBefore, isAfter } from "validator";
import { FormularioCargo } from "../Cargo";

const anoAtual = new Date().getFullYear();
const maxData = `${anoAtual - 15}-12-31`;
const minData = `${anoAtual - 100}-01-01`;

/**
 * Componente para cadastrar ou alterar um usuário.
 * Este componente permite ao usuário cadastrar um novo usuario ou alterar os dados de um usuário existente.
 * 
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar um usuário.
 */
const FormularioUsuario = () => {
  const { control, register, setError, getValues, handleSubmit, clearErrors, watch, reset, formState: { errors } } = useForm({
    shouldFocusError: false,
    defaultValues: {
      cargos: [],
      tipo: "p"
    },
  });
  const { fields, append, remove } = useFieldArray({ control, name: "cargos" });
  const tipo = watch("tipo");
  const senha = watch("senha");

  // Configuração padrão
  const [alterar, setAlterar] = useState(false);
  const api = useApi("/api");
  const navigate = useNavigate();
  const { chave } = useParams();

  // const validateArrayNotEmpty = (value) => {

  //   if (fields.length === 0) {
  //     setError("cargos", { type: "void"});
  //     return false; // Impede o envio do formulário
  //   }
  //   clearErrors("cargos"); // Limpa o erro se o array não estiver vazio
  //   return true;
  // };

  /**
   * Função para lidar com o envio do formulário.
   * Dependendo do caminho da URL, a função irá cadastrar um novo usuário ou alterar um usuário existente.
   * 
   * @param {Event} event - O evento de submissão do formulário.
   */
  const enviarFormulario = async (data) => {

    if (fields.length === 0) {
      setError("cargos", { type: "void"});
      return;
    }
      
    clearErrors("cargos");

    data.cpf = data.cpf.replace(/\D/g, '');
    data.disciplinas = data.disciplinas.split(',').map((disciplina) => disciplina.trim());

    try {
      if (location.pathname.includes("alterar")) {
        await api.updateData(`/usuario/${chave}`, data);

        navigate(`/usuario/${data.cpf}?success=true`);
      } else {
        await api.createData("/usuario", data);

        navigate("/usuario?success=true&type=cadastro");
      }
    } catch (error) {

      if (error.message == "Usuário já existe") {
        setError("cpf", { type: "equal" });
      }

      console.log(error.message.includes("Disciplinas inválidas"));

      if (error.message.includes("Disciplinas inválidas")) {
        setError("disciplinas", { type: "absence" });
      }

      console.error(error.message);
    }

  };

  /**
     * Função para, na alteração, voltar a página de informações
     */
    const funcaoVoltar = () => navigate(`/usuario/${cpf}`);
  
    // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
    if (alterar && api.loading) return <p>Carregando...</p>;
  
    // Exibe mensagem de erro caso ocorra um erro na requisição
    if (alterar && api.error) return <p>Erro: {api.error}</p>;
  
    return (
      <Container fluid className="d-flex flex-column h-100 overflow-y-auto">
        <Titulo>{alterar? "Alterar" : "Cadastrar"} Usuário</Titulo>
        <Form className="flex-fill d-flex flex-column justify-content-between mt-4" onSubmit={handleSubmit(enviarFormulario)}>
          <Container fluid className="d-grid gap-3">
            <Row className="gap-5">
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="nome" data-testid="nome">Nome: <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    id="nome"
                    type="text"
                    className="p-2"
                    placeholder="Exemplo: Cristóvão Colombo"
                    {...register('nome', { required: true, minLength: 3, maxLength: 100 })}
                  /> 
                  <Alert variant="white" className={`${errors.nome? "" : "d-none"} text-danger`}>
                    {errors?.nome?.type == "required" && "O nome é obrigatório"}
                    {errors?.nome?.type == "minLength" && "O nome deve ter no mínimo 3 caracteres"}
                    {errors?.nome?.type == "maxLength" && "O nome deve ter no máximo 100 caracteres"}
                  </Alert>
                </Form.Group>
              </Col>
            </Row>
            <Row className="gap-5">
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="email">Email: <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    id="email"
                    type="text"
                    className="p-2"
                    placeholder="Exemplo: criscolombo@terra.com.br"
                    {...register('email', { required: true, minLength: 3, maxLength: 100,  validate: (value) => isEmail(value)})}
                  />
                  <Alert variant="white" className={`${errors.email? "" : "d-none"} text-danger`}>
                    {errors?.email?.type == "required" && "O email é obrigatório"}
                    {errors?.email?.type == "minLength" && "O email deve ter no mínimo 3 caracteres"}
                    {errors?.email?.type == "maxLength" && "O email deve ter no máximo 100 caracteres"}
                    {errors?.email?.type == "validate" && "O email está no formato errado ou não é um email válido"}
                  </Alert>
                </Form.Group>
              </Col>
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="cpf">CPF: <span className="text-danger">*</span></Form.Label>
                  <Controller
                    name="cpf"
                    control={control}
                    defaultValue=""
                    rules={{ required: true }}
                    render={({ field }) => (
                      <IMaskInput
                        {...field}
                        id="cpf"
                        mask="000.000.000-00"
                        placeholder="Exemplo: 999.888.777-66"
                        className="p-2 form-control"
                      />
                    )}
                  />
                  <Alert variant="white" className={`${errors.cpf? "" : "d-none"} text-danger`}>
                    {errors?.cpf?.type == "equal" && "Já existe um usuário com esse CPF"}
                    {errors?.cpf?.type == "required" && "O CPF é obrigatório"}
                  </Alert> 
                </Form.Group>
              </Col>
            </Row>
            <Row className="gap-5">
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
                    {errors?.data_de_nascimento?.type == "validate" && "O usuário deve ter entre 15 e 100 anos"}
                  </Alert>
                </Form.Group>
              </Col>
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="telefone">Telefone:</Form.Label>
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
                    {errors?.telefone?.type == "maxLength" && "O telefone deve ter no máximo 50 caracteres"}
                    {errors?.telefone?.type == "pattern" && "Formato de telefone inválido. Utilize o formato: 99 9 9999-9999"}
                  </Alert>
                </Form.Group>
              </Col>
            </Row>
            <Row className="gap-5">
                <Col>
                  <Form.Group className="d-flex flex-column gap-1">
                    <Form.Label htmlFor="horarioTrabalho">Horário de Trabalho: <span className="text-danger">*</span></Form.Label>
                    <Form.Control
                      id="horarioTrabalho"
                      type="text"
                      className="p-2"
                      placeholder="Exemplo: Seg-Sex,12h-17h"
                      {...register('horario_de_trabalho', { required: true, minLength: 5, maxLength: 20, pattern: /^[A-Z][a-z]{2}-[A-Z][a-z]{2},([01]\d|2[0-3])h-([01]\d|2[0-3])h$/ })}
                    />
                    <Alert variant="white" className={`${errors.horario_de_trabalho? "" : "d-none"} text-danger`}>
                      {errors?.horario_de_trabalho?.type == "required" && "O horário de trabalho é obrigatório"}
                      {errors?.horario_de_trabalho?.type == "minLength" && "O horário de trabalho deve ter no mínimo 5 caracteres"}
                      {errors?.horario_de_trabalho?.type == "maxLength" && "O horário de trabalho deve ter no máximo 20 caracteres"}
                      {errors?.horario_de_trabalho?.type === "pattern" && "Formato inválido. Exemplo: 'Seg-Sex,07h-18h'. Os valores dos dias podem ser Seg, Ter, Qua, Qui, Sex"}
                  </Alert>
                  </Form.Group>
                </Col>
                <Col>
                  <Form.Group className="d-flex flex-column gap-1">
                    <Form.Label htmlFor="tipo">Tipo: <span className="text-danger">*</span></Form.Label>
                    <Form.Select 
                      id="tipo" 
                      className="p-2" 
                      {...register('tipo', { required: true })}>
                      <option value="p">Professor</option>
                      <option value="f">Funcionário</option>
                    </Form.Select>
                  </Form.Group>
                </Col>
            </Row>
            <Row className="gap-5">
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="endereco">Endereço:</Form.Label>
                  <Form.Control
                    id="endereco"
                    as="textarea"
                    style={{ resize: 'none' }}
                    className="p-2"
                    placeholder="Exemplo: Rua das Flores, N° 24, Bairro Industrial, Carira/SE"
                    {...register('endereco', { required: false, minLength: 10, maxLength: 255 })}
                  />
                  <Alert variant="white" className={`${errors.endereco? "" : "d-none"} text-danger`}>
                    {errors?.endereco?.type == "minLength" && "O endereço deve ter no mímimo 10 caracteres"}
                    {errors?.endereco?.type == "maxLength" && "O endereço deve ter no máximo 255 caracteres"}
                  </Alert>
                </Form.Group>
              </Col>
            </Row>
            <Row className="gap-5">
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="senha" data-testid="senha">Senha: <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    id="senha"
                    type="password"
                    className="p-2"
                    placeholder="No mínimo 5 caracteres"
                    {...register('senha', { required: true, minLength: 5, maxLength: 100 })}
                  />
                  <Alert variant="white" className={`${errors.senha? "" : "d-none"} text-danger`}>
                    {errors?.senha?.type == "required" && "A senha é obrigatória"}
                    {errors?.senha?.type == "minLength" && "A senha deve ter no mínimo 5 caracteres"}
                    {errors?.senha?.type == "maxLength" && "A senha deve ter no máximo 100 caracteres"}
                  </Alert>
                </Form.Group>
              </Col>
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="Confsenha">Confirmar senha: <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    id="Confsenha"
                    type="password"
                    className="p-2"
                    placeholder="Digite a senha novamente"
                    {...register('confirmar_senha', { required: true, minLength: 5, maxLength: 100, validate: (value) => value == senha })}
                  />
                  <Alert variant="white" className={`${errors.confirmar_senha? "" : "d-none"} text-danger`}>
                    {errors?.confirmar_senha?.type == "required" && "A senha a ser confirmada é obrigatória"}
                    {errors?.confirmar_senha?.type == "validate" && "As senhas não correspondem"}
                  </Alert>
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <FormularioCargo 
                fields={fields}
                append={append}
                remove={remove}
                erro={errors}
                setError={setError}
                clearErrors={clearErrors}
              />
            </Row>
            <Row className={`${tipo == "p"? "" : "d-none"} gap-5`}>
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="formacao">Formação: <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    id="formacao"
                    type="text"
                    className="p-2"
                    placeholder="Exemplo: Bacharelado em Matemática"
                    {...register('formacao', { required: tipo == "p", minLength: 10, maxLength: 255 })}
                  />
                  <Alert variant="white" className={`${errors.formacao? "" : "d-none"} text-danger`}>
                    {errors?.formacao?.type == "required" && tipo == "p" && "A formação do professor é obrigatória"}
                    {errors?.formacao?.type == "minLength" && "A formacão deve ter no mínimo 10 caracteres"}
                    {errors?.formacao?.type == "maxLength" && "A formação deve ter no máximo 255 caracteres"}
                  </Alert>
                </Form.Group>
              </Col>
            </Row>
            <Row className={`${tipo == "p"? "" : "d-none"} gap-5`}>
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="codigosDisciplinas">Código(s) da(s) Disciplinas: <span className="text-danger">*</span></Form.Label>
                    <Form.Control
                      id="codigosDisciplinas"
                      type="text"
                      className="p-2"
                      placeholder="Exemplo: MAT101,FIS202,QUI303"
                      {...register('disciplinas', { required: tipo == "p", minLength: 6 })}
                    />
                    <Alert variant="white" className={`${errors.disciplinas? "" : "d-none"} text-danger`}>
                      {errors?.disciplinas?.type == "required" && tipo == "p" && "As disciplinas do professor são obrigatórias"}
                      {errors?.disciplinas?.type == "absence" && "As disciplinas não existem"}
                      {errors?.disciplinas?.type == "minLength" && "Ao menos uma disciplina deve ser cadastrada"}
                  </Alert>
                </Form.Group>
              </Col>
            </Row>
            <Row className={`${tipo == "f"? "" : "d-none"} gap-5`}>
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="habilidades">Habilidades: <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    id="habilidades"
                    type="text"
                    className="p-2"
                    placeholder="Exemplo: Informática Básica, Inglês Básico"
                    {...register('habilidades', { required: tipo == "f", minLength: 10, maxLength: 255 })}
                  />
                  <Alert variant="white" className={`${errors.habilidades? "" : "d-none"} text-danger`}>
                    {errors?.habilidades?.type == "required" && tipo == "f" && "As habilidades do funcionário são obrigatórias"}
                    {errors?.habilidades?.type == "minLength" && "As habilidades devem ter no mínimo 10 caracteres"}
                    {errors?.habilidades?.type == "maxLength" && "As habilidades devem ter no máximo 255 caracteres"}
                  </Alert>
                </Form.Group>
              </Col>
            </Row>
            <Row className={`${tipo == "f"? "" : "d-none"} gap-5`}>
              <Col>
                <Form.Group className="d-flex flex-column gap-1">
                  <Form.Label htmlFor="escolaridade">Escolaridade: <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    id="escolaridade"
                    type="text"
                    className="p-2"
                    placeholder="Exemplo: Ensino Superior Completo"
                    {...register('escolaridade', { required: tipo == "f", minLength: 5, maxLength: 255 })}
                  />
                  <Alert variant="white" className={`${errors.escolaridade? "" : "d-none"} text-danger`}>
                    {errors?.escolaridade?.type == "required" && tipo == "f" && "A escolaridade do funcionário é obrigatória"}
                    {errors?.escolaridade?.type == "minLength" && "A escolaridade deve ter no mínimo 5 caracteres"}
                    {errors?.escolaridade?.type == "maxLength" && "A escolaridade deve ter no máximo 255 caracteres"}
                  </Alert>
                </Form.Group>
              </Col>
            </Row>
          </Container>
          <Container fluid className="mt-3">
            {
              alterar? <BotaoAlterar funcaoVoltar={funcaoVoltar} /> : <BotaoCadastrar />
            }
          </Container>
        </Form>
      </Container>
    );
  };
  
  export default FormularioUsuario;