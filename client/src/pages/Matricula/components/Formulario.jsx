import React, { useState } from "react";
import { Container, Form } from "react-bootstrap";
import { useForm } from "react-hook-form";
import { Botao } from "../../../components/Botao";
import { Alert } from "@mui/material";

const Formulario = ({ enviarFormulario }) => {
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm();
  const [loading, setLoading] = useState(false);

  const onSubmit = async (data) => {
    setLoading(true);

    try {
      await enviarFormulario(data);
    } catch (e) {
      if (e.message.includes("Não existe aluno com essa matrícula")) {
        setError("aluno_matricula", { type: "void" });
      }

      if (e.message.includes("Não existe turma com esse id")) {
        setError("turma_id", { type: "void" });
      }

      if (e.message.includes("A turma informada não está ativa")) {
        setError("turma_id", {
          type: "invalid",
          message: "A turma informada não está ativa",
        });
      }

      if (e.message.includes("Aluno já está matriculado nessa turma")) {
        setError("turma_id", {
          type: "invalid",
          message: "Aluno já está matriculado nessa turma",
        });
      }

      if (
        e.message.includes(
          "O aluno já está matriculado em uma turma nesse ano letivo"
        )
      ) {
        setError("root.serverError", {
          message: "O aluno já está matriculado em uma turma nesse ano letivo",
        });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      {errors.root && <Alert severity="error">{errors.root.message}</Alert>}
      <Container fluid className="my-3 d-grid gap-3">
        <Form.Group className="d-flex flex-column gap-1">
          <Form.Label htmlFor="matricula">
            Matrícula do aluno: <span className="text-danger">*</span>
          </Form.Label>
          <Form.Control
            id="matricula"
            type="text"
            className="p-2"
            placeholder="Exemplo: 202500001223"
            {...register("aluno_matricula", {
              required: true,
              minLength: 12,
              maxLength: 12,
            })}
          />
          <Container
            className={`${
              errors.aluno_matricula ? "" : "d-none"
            } py-2 text-danger`}
          >
            {errors.aluno_matricula?.type == "required" &&
              "A matrícula do aluno é obrigatória"}
            {(errors.aluno_matricula?.type == "minLength" ||
              errors.aluno_matricula?.type == "maxLength") &&
              "A matrícula do aluno deve ter exatamente 12 caracteres"}
            {(errors.aluno_matricula?.type == "void") &&
              "O aluno não existe"}
          </Container>
        </Form.Group>
        <Form.Group className="d-flex flex-column gap-1">
          <Form.Label htmlFor="id-turma">
            Id da turma: <span className="text-danger">*</span>
          </Form.Label>
          <Form.Control
            id="id-turma"
            type="number"
            className="p-2"
            placeholder="Exemplo: 1230"
            {...register("turma_id", {
              required: true,
              min: 1,
              valueAsNumber: true,
            })}
          />
          <Container
            className={`${errors.turma_id ? "" : "d-none"} py-2 text-danger`}
          >
            {errors.turma_id?.type == "required" &&
              "O id da turma é obrigatório"}
            {errors.turma_id?.type == "min" &&
              "O id da turma não pode ser menor que 1"}
            {errors.turma_id?.type == "void" &&
              "A turma não existe"}
            {errors.turma_id?.type == "invalid" &&
            errors.turma_id?.message}
          </Container>
        </Form.Group>
        <p>
          Os campos com <span className="text-danger">*</span> são obrigatórios.
        </p>
        <Botao.Group>
          <Botao.Base
            title={!loading ? "Matricular" : "Matriculando..."}
            type="submit"
          />
        </Botao.Group>
      </Container>
    </Form>
  );
};

export default Formulario;
