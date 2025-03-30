import React, { useEffect } from "react";
import { Col, Container, Form, Row } from "react-bootstrap";
import { useForm } from "react-hook-form";
import BotaoBase from "../../../components/Botao/BotaoBase";
import useApi from "../../../hooks/useApi";

const Buscar = ({ realizarBusca }) => {
  const { register, handleSubmit, watch } = useForm();
  const { fetchData, data } = useApi("/api");

  const turma = watch("turma");

  useEffect(() => {
    const carregarDados = async () => {
      try {
        await fetchData("/boletim");
      } catch (err) {
        console.error(err)
      }
    }

    carregarDados();
  }, [])

  const onSubmit = async (data) => {
    try {
      await realizarBusca(data);
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
          <Col className="col-5">
            <Form.Group>
              <Form.Label htmlFor="disciplina-select">Disciplina:</Form.Label>
              <Form.Select
                id="disciplina-select"
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
