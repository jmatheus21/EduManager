import React from "react";
import { Col, Container, Form, Row } from "react-bootstrap";
import { useForm } from "react-hook-form";
import BotaoBase from "../../../components/Botao/BotaoBase";

const Buscar = ({ data, realizarBusca }) => {
  const { register, handleSubmit, watch } = useForm();

  const turma = watch("turma");

  const onSubmit = async (dados) => {
    try {
      await realizarBusca(dados);
    } catch (err) {
      console.error(err.message);
    }
  };

  return (
    <Container fluid className="my-4">
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Row className="gap-3 mb-3">
          <Col className="col-5">
            <Form.Group>
              <Form.Label htmlFor="turma">Turma:</Form.Label>
              <Form.Select id="turma" className="p-2" {...register("turma")}>
                <option value="">Selecione uma turma</option>
                {data?.turmas.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.ano}° ano {item.serie} - {item.nivel_de_ensino}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
          </Col>
          <Col className="col-5">
            <Form.Group>
              <Form.Label htmlFor="disciplina">Disciplina:</Form.Label>
              <Form.Select
                id="disciplina"
                disabled={!turma}
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
          <Col className="d-flex align-items-end justify-content-end">
            <BotaoBase title={"Buscar"} type="submit" />
          </Col>
        </Row>
      </Form>
    </Container>
  );
};

export default Buscar;
