import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Form, Container } from "react-bootstrap"
import { Botao } from "../../../components/Botao";
import { Alert } from "@mui/material"

export default function FormularioAluno({ aluno, enviarFormulario }) {
    const { register, handleSubmit, reset, formState: { errors } } = useForm({
      defaultValues: {
        ausencias: aluno?.ausencias || 0
      }
    });

    useEffect(() => {
      reset({
        ausencias: aluno?.ausencias || 0
      });
    }, [aluno, reset]);
  
    const handleSave = async (data) => {
      try {
        await enviarFormulario(data);
      } catch (e) {
        console.error(e);
      }
    };
  
    return (
      <Form onSubmit={handleSubmit(handleSave)} className="w-100">
        <p className="d-flex gap-1 my-3"><strong>Nome:</strong> <span>{aluno?.nome}</span></p>
        <Container className="d-flex justify-content-center align-items-center flex-column gap-3">
          <Form.Group className="border border-2 rounded-1 p-3 w-30">
            <Form.Label htmlFor="ausencias" className="fs-5 fw-bold d-block text-center mb-1">Ausências</Form.Label>
            <Form.Control
              id="ausencias"
              type="number"
              className="p-2 text-center"
              min="0"
              {...register("ausencias", { required: true, valueAsNumber: true, min: 0, max: 100 })}
            />
          </Form.Group>
          {errors.ausencias && (
            <Alert severity="error" className="p-2 d-flex gap-3">
              {errors?.ausencias?.type == "required" && "Ausências é obrigatório"}
              {errors?.ausencias?.type == "min" && "Ausências não pode ser um valor negativo"}
              {errors?.ausencias?.type == "max" && "Ausências não pode ultrapassar o valor de 100"}
            </Alert>
          )}
        </Container>
        <Botao.Group>
          <Botao.Base title="Salvar" type="submit" />
        </Botao.Group>
      </Form>
    );
  }