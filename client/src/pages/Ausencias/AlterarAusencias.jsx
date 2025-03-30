import React, { useEffect, useState } from "react";
import FormularioAluno from "./components/FormularioAluno";
import { Container } from "react-bootstrap";
import BuscarAluno from "./components/BuscarAluno";
import useApi from "../../hooks/useApi";
import { Titulo } from "../../components";
import { Alert } from "@mui/material";

const AlterarAusencias = () => {
  const { fetchData, updateData, data } = useApi("/api");
  const buscarApi = useApi("/api");
  const [show, setShow] = useState(false);
  const [message, setMessage] = useState("");
  const [type, setType] = useState("success");

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

  const realizarBusca = async (dados) => {
    try {
      const response = await fetchData(
        `/ausencias/${dados.aula_id}/${dados.aluno_matricula}`
      );

      if (response) {
        setShow(true);
        setMessage("");
      }
    } catch (e) {
      setMessage(e.message);
      setType("error");
      setShow(false);

      setTimeout(() => {
        setMessage("");
        setShow(false);
      }, 3000);

      throw new Error(e.message);
    }
  };

  const enviarFormulario = async (dados) => {
    try {
      const response = await updateData(
        `/ausencias/${data.aula_id}/${data.matricula}`,
        dados
      );

      if (response) {
        setMessage("Ausências alteradas com sucesso!");
        setType("success");
  
        setTimeout(() => {
          setMessage("");
          setShow(false);
        }, 3000);
      }
    } catch (e) {
      throw new Error(e.message);
    }
  };

  return (
    <Container fluid>
      <Titulo>Alterar Ausências</Titulo>
      <BuscarAluno data={buscarApi.data} realizarBusca={realizarBusca} />
      {message && (
        <Alert severity={type} className="p-3 d-flex gap-3">
          {message}
        </Alert>
      )}
      {show ? (
        <FormularioAluno aluno={data} enviarFormulario={enviarFormulario} />
      ) : (
        <p className="d-flex justify-content-center mt-3">
          Selecione uma turma, uma disciplina e uma matrícula.
        </p>
      )}
    </Container>
  );
};

export default AlterarAusencias;
