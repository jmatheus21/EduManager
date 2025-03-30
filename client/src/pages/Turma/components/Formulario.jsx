import React, { useEffect } from "react";
import { Col, Form, Row, Alert, Container } from "react-bootstrap";
import { useNavigate } from "react-router";
import { useForm } from "react-hook-form";
import { Botao } from "../../../components/Botao";

const anoAtual = new Date().getFullYear();

/**
 * Componente para cadastrar ou alterar uma turma.
 * Este componente permite ao usuário cadastrar uma nova turma ou alterar os dados de uma turma existente.
 *
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar uma turma.
 */
const Formulario = ({ enviarFormulario, alteracao }) => {
  const {
    register,
    handleSubmit,
    reset,
    setError,
    formState: { errors },
  } = useForm();
  const { alterar, dados, chave } = alteracao;
  const navigate = useNavigate();

  /**
   * Efeito para carregar os dados da turma quando o componente é montado ou quando o caminho da URL ou o parâmetro `chave` mudam.
   * Se o caminho da URL incluir "alterar", o título do formulário será alterado para "Alterar" e os dados da turma serão carregados.
   */
  useEffect(() => {
    const carregarDados = async () => {
      if (alterar && dados) {
        reset(dados);
      }
    };

    carregarDados();
  }, [alterar, dados, reset]);

  /**
   * Função para lidar com o envio do formulário.
   * Dependendo do caminho da URL, a função irá cadastrar uma nova turma ou alterar uma turma existente.
   *
   * @param {Event} event - O evento de submissão do formulário.
   */
  const onSubmit = async (data) => {
    try {
      await enviarFormulario(data);
    } catch (error) {
      console.error("A mensagem do erro: ", error.message);

      if (error.message.includes("Turma já existe")) {
        setError("root.serverError", {
          message: "Já existe uma turma com esses dados",
        });
      }

      if (error.message.includes("Já existe uma turma no mesmo horário")) {
        setError("root.serverError", {
          message: "Já existe uma turma no mesmo horário",
        });
      }

      if (error.message.includes("Calendário não existe")) {
        setError("calendario_ano_letivo", { type: "void" });
      }

      if (error.message.includes("Sala não existe")) {
        setError("sala_numero", { type: "void" });
      }
    }
  };

  /**
   * Função para, na alteração, voltar a página de informações
   */
  const funcaoVoltar = () => navigate(`/turma/${chave}`);

  return (
    <Form
      className="flex-fill d-flex flex-column justify-content-between mt-4"
      onSubmit={handleSubmit(onSubmit)}
    >
      <Alert
        variant={"danger"}
        className={`${errors.root ? "" : "d-none"} text-center py-1 mb-3`}
      >
        {errors?.root?.serverError && (
          <p>{errors?.root?.serverError?.message}</p>
        )}
      </Alert>
      <Container fluid className="d-grid gap-3">
        <Row className="gap-5">
          <Col>
            <Form.Group className="d-flex flex-column gap-1">
              <Form.Label htmlFor="ano">
                Ano: <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                id="ano"
                type="number"
                className="p-2"
                placeholder="Exemplo: 1"
                {...register("ano", {
                  required: true,
                  min: 1,
                  max: 9,
                  valueAsNumber: true,
                })}
              />
            </Form.Group>
            <Alert
              variant="white"
              className={`${errors.ano ? "" : "d-none"} text-danger`}
            >
              {errors?.ano?.type == "required" &&
                "O ano da turma é obrigatório"}
              {errors?.ano?.type == "min" &&
                "O ano da turma deve ser no mínimo 1"}
              {errors?.ano?.type == "max" &&
                "O ano da turma deve ser no máximo 9"}
            </Alert>
          </Col>
          <Col>
            <Form.Group className="d-flex flex-column gap-1">
              <Form.Label htmlFor="serie">
                Série: <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                id="serie"
                type="text"
                className="p-2"
                placeholder="Exemplo: A"
                {...register("serie", {
                  required: true,
                  maxLength: 1,
                  pattern: /^[A-Z]$/,
                })}
              />
            </Form.Group>
            <Alert
              variant="white"
              className={`${errors.serie ? "" : "d-none"} text-danger`}
            >
              {errors?.serie?.type == "required" && "A série é obrigatória"}
              {errors?.serie?.type == "maxLength" &&
                "A série deve ter no máximo 1 caractere"}
              {errors?.serie?.type === "pattern" &&
                "A série deve ser uma letra (A-Z)"}
            </Alert>
          </Col>
        </Row>
        <Row className="gap-5">
          <Col>
            <Form.Group className="d-flex flex-column gap-1">
              <Form.Label htmlFor="nivel_de_ensino">
                Nível de Ensino: <span className="text-danger">*</span>
              </Form.Label>
              <Form.Select
                id="nivel_de_ensino"
                type="text"
                className="p-2"
                {...register("nivel_de_ensino", {
                  required: true,
                  minLength: 2,
                  maxLength: 30,
                })}
              >
                <option value="">Selecione...</option>
                <option value="Ensino Fundamental">Ensino Fundamental</option>
                <option value="Ensino Médio">Ensino Médio</option>
              </Form.Select>
            </Form.Group>
            <Alert
              variant="white"
              className={`${
                errors.nivel_de_ensino ? "" : "d-none"
              } text-danger`}
            >
              {errors?.nivel_de_ensino?.type == "required" &&
                "O nível de ensino é obrigatório"}
              {errors?.nivel_de_ensino?.type == "minLength" &&
                "O nível de ensino deve ter no mínimo 2 caracteres"}
              {errors?.nivel_de_ensino?.type == "maxLength" &&
                "O nível de ensino deve ter no máximo 30 caracteres"}
            </Alert>
          </Col>
          <Col>
            <Form.Group className="d-flex flex-column gap-1">
              <Form.Label htmlFor="turno">
                Turno: <span className="text-danger">*</span>
              </Form.Label>
              <Form.Select
                id="turno"
                type="text"
                className="p-2"
                {...register("turno", { required: true, maxLength: 1 })}
              >
                <option value="">Selecione...</option>
                <option value="M">Matutino</option>
                <option value="V">Vespertino</option>
                <option value="N">Noturno</option>
              </Form.Select>
            </Form.Group>
            <Alert
              variant="white"
              className={`${errors.turno ? "" : "d-none"} text-danger`}
            >
              {errors?.turno?.type == "required" && "O turno é obrigatório"}
              {errors?.turno?.type == "maxLength" &&
                "O turno deve ter no máximo 1 caractere"}
            </Alert>
          </Col>
        </Row>
        <Row className="gap-5">
          <Col>
            <Form.Group className="d-flex flex-column gap-1">
              <Form.Label htmlFor="sala_numero">
                Número da Sala: <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                id="sala_numero"
                type="int"
                className="p-2"
                placeholder="Exemplo: 123"
                {...register("sala_numero", {
                  required: true,
                  min: 1,
                  max: 1000,
                  valueAsNumber: true,
                })}
              />
            </Form.Group>
            <Alert
              variant="white"
              className={`${errors.sala_numero ? "" : "d-none"} text-danger`}
            >
              {errors?.sala_numero?.type == "required" &&
                "O número da sala é obrigatório"}
              {errors?.sala_numero?.type == "min" &&
                "O número da sala deve ser no mínimo 1"}
              {errors?.sala_numero?.type == "max" &&
                "O número da sala deve ser de no máximo 1000"}
              {errors?.sala_numero?.type == "void" && "A sala não existe"}
            </Alert>
          </Col>
          <Col>
            <Form.Group className="d-flex flex-column gap-1">
              <Form.Label htmlFor="calendario_ano_letivo">
                Ano Letivo: <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                id="calendario_ano_letivo"
                type="int"
                className="p-2"
                placeholder="Exemplo: 2026"
                {...register("calendario_ano_letivo", {
                  required: true,
                  validate: (value) => value >= anoAtual,
                  valueAsNumber: true,
                })}
              />
            </Form.Group>
            <Alert
              variant="white"
              className={`${
                errors.calendario_ano_letivo ? "" : "d-none"
              } text-danger`}
            >
              {errors?.calendario_ano_letivo?.type == "required" &&
                "O ano letivo é obrigatório"}
              {errors?.calendario_ano_letivo?.type == "validate" &&
                `O ano deve ser igual ou maior que ${anoAtual}`}
              {errors?.calendario_ano_letivo?.type == "void" &&
                "O ano letivo não existe"}
            </Alert>
          </Col>
        </Row>
        <Row>
          <p>
            Os campos com <span className="text-danger">*</span> são
            obrigatórios.
          </p>
        </Row>
      </Container>
      {alterar ? (
        <Botao.Group>
          <Botao.Base
            title={"Voltar"}
            sx={{ bgcolor: "grey.600", color: "white" }}
            onClick={funcaoVoltar}
          />
          <Botao.Base title={"Alterar"} type="submit" />
        </Botao.Group>
      ) : (
        <Botao.Group>
          <Botao.Base title={"Finalizar"} type="submit" />
        </Botao.Group>
      )}
    </Form>
  );
};

export default Formulario;
