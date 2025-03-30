import React, { useState, useEffect } from "react";
import FormularioCadastro from "./components/FormularioCadastro";
import { Container } from "react-bootstrap";
import Buscar from "./components/Buscar";
import useApi from "../../hooks/useApi";
import { Titulo } from "../../components";
import { Alert } from "@mui/material";

const CadastrarNotas = () => {
  const { fetchData, createData, data } = useApi("/api");
  const buscarApi = useApi("/api");
  const [show, setShow] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const carregarDados = async () => {
      try {
        await buscarApi.fetchData("/boletim");
      } catch (err) {
        console.error(err);
      }
    };

    carregarDados();
  }, []);

  const realizarBusca = async (data) => {
    try {
      await fetchData(`/notas/${data.aula_id}`);
    } catch (e) {
      console.error(e);
    } finally {
      setShow(true);
    }
  };

  const enviarFormulario = async (dados) => {
    dados = { ...dados, aula_id: data.aula_id };

    try {
      await createData("/notas", dados);

      setMessage("Notas cadastradas com sucesso!");

      setTimeout(() => {
        setMessage("");
        setShow(false);
      }, 3000);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <Container fluid>
      <Titulo>Cadastrar Notas</Titulo>
      <Buscar data={buscarApi.data} realizarBusca={realizarBusca} />
      {message && (
        <Alert severity="success" className="p-3 d-flex gap-3">
          {message}
        </Alert>
      )}
      {show ? (
        <FormularioCadastro
          alunos={data?.alunos}
          enviarFormulario={enviarFormulario}
        />
      ) : (
        <p className="d-flex justify-content-center">
          Selecione uma turma e uma disciplina
        </p>
      )}
    </Container>
  );
};

export default CadastrarNotas;
