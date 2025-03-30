import React, { useEffect } from "react";
import { Col, Container, Form, Row, Alert } from "react-bootstrap";
import { useForm } from "react-hook-form";
import BotaoBase from "../../../components/Botao/BotaoBase";
import useApi from "../../../hooks/useApi";

const BuscarAluno = ({ data, realizarBusca }) => {
  const { register, handleSubmit, watch, formState: { errors } } = useForm();

  const turma = watch("turma");

  const onSubmit = async (data) => {
    try {
      await realizarBusca(data);
    } catch (err) {
      if (err.message.includes("Aluno não existe")) {
        setError("aluno_matricula", { type: "void" });
      }
    }
  };

  return (
    <Container fluid className="my-4 p-3 border border-3 rounded-1">
      <Form onSubmit={handleSubmit(onSubmit)} className="d-flex flex-column gap-3">
        <Row className="justify-content-between mb-3 gap-3 gap-md-0">
          <Col md={6} className="col-12">
            <Form.Group className='d-flex gap-2 align-items-center pe-md-2 pe-0'>
              <Form.Label htmlFor="turma-select">Turma:</Form.Label>
              <Form.Select
                id="turma-select"
                className="p-2"
                {...register("turma")}
              >
                <option value="">Selecione uma turma</option>
                {data?.turmas.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.ano}° ano {item.serie} - {item.nivel_de_ensino}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={6} className="col-12">
            <Form.Group className='d-flex gap-2 align-items-center ps-0 ps-md-2'>
              <Form.Label htmlFor="disciplina-select">Disciplina:</Form.Label>
              <Form.Select
                disabled={!turma}
                id="disciplina-select"
                className="p-2"
                {...register("aula_id")}
              >
                <option value="">Selecione uma disciplina</option>
                {data?.disciplinas.map((item) => {
                  if (item.turma_id == turma) {
                    return (
                      <option key={item.codigo} value={item.aula_id}>
                        {item.nome} ({item.codigo})
                      </option>
                    );
                  }
                })}
              </Form.Select>
            </Form.Group>
          </Col>
        </Row>
        <Row className="justify-content-between gap-3 gap-md-0">
          <Col md={10} xl={11} className="col-12">
            <Form.Group className="d-flex gap-2 align-items-center pe-xl-3 pe-0">
              <Form.Label htmlFor="matricula">Matrícula: </Form.Label>
              <Form.Control
                id="matricula"
                type="text"
                className="p-2"
                {...register("aluno_matricula", { required: true, minLength: 12, maxLength: 12 })}
              />
              <Alert variant='white' className={`${errors.aluno_matricula? "" : "d-none"} py-2 text-danger`}>
                    { errors.aluno_matricula?.type == "required" && "A matrícula do aluno é obrigatória" }
                    { (errors.aluno_matricula?.type == "minLength" ||  errors.aluno_matricula?.type == "maxLength") && "A matrícula do aluno deve ter exatamente 12 caracteres" }
                    { errors.aluno_matricula?.type == "void" && "O aluno não existe" }
              </Alert>
            </Form.Group>
          </Col>
          <Col md={2} xl={1} className="d-flex align-items-end justify-content-end col-12">
            <BotaoBase title={"Buscar"} type="submit" />
          </Col>
        </Row>
      </Form>
    </Container>
  );
};

export default BuscarAluno;
