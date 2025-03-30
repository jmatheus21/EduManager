import React, { useState } from "react";
import Formulario from "./components/Formulario.jsx";
import { Container } from "react-bootstrap";
import Buscar from "./components/Buscar";
import useApi from "../../hooks/useApi";
import { Titulo } from "../../components";
import { Alert } from "@mui/material";

const RegistroAusencias = () => {
  const { fetchData, updateData, data } = useApi("/api");
  const [show, setShow] = useState(false);
  const [message, setMessage] = useState("");

  const realizarBusca = async (data) => {
    try {
      await fetchData(`/ausencias/${data.aula_id}`);
    } catch (e) {
      throw new Error(e.message);
    } finally {
      setShow(true);
    }
  };

  const enviarFormulario = async (dados) => {
    dados = {...dados, aula_id: data.aula_id};

    try {
      await updateData(`/ausencias/${dados.aula_id}`, dados);
      
      setMessage("Ausências registradas com sucesso!");

      setTimeout(() => {
        setMessage("");
        setShow(false);
      }, 3000)
    } catch (e) {
      throw new Error(e.message);
    }
  };

  return (
    <Container fluid>
      <Titulo>Registrar Ausências</Titulo>
      <Buscar realizarBusca={realizarBusca} />
      {message && <Alert severity="success" className="p-3 d-flex gap-3">{message}</Alert>}
      {show ? (
        <Formulario
          alunos={data?.alunos}
          enviarFormulario={enviarFormulario}
        />
      ) : (
        <p className="d-flex justify-content-center">Selecione uma turma e uma disciplina</p>
      )}
    </Container>
  );
};

export default RegistroAusencias;