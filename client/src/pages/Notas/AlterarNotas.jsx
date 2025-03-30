import React, { useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import { Titulo } from "../../components";
import BuscarAlterar from "./components/BuscarAlterar";
import useApi from "../../hooks/useApi";
import FormularioAlterar from "./components/FormularioAlterar";
import { Alert } from "@mui/material";

const AlterarNotas = () => {
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
      const response = await fetchData(`/notas/${dados.aluno_matricula}/${dados.aula_id}`);

      if (response) {
        setShow(true);
        setMessage("");
      }
    } catch (e) {
      setShow(e.message)
      setType("error");
      setShow(false);

      setTimeout(() => {
        setMessage("");
        setShow(false);
      }, 3000);
    }
  };

  const enviarFormulario = async (dados) => {
    try {
      const response = await updateData(`/notas/${data.matricula}/${data.aula_id}`, dados);

      if (response) {
        setMessage("Notas alteradas com sucesso!");
        setType("success");
  
        setTimeout(() => {
          setMessage("");
          setShow(false);
        }, 3000);
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <Container fluid>
      <Titulo>Alterar Notas</Titulo>
      <BuscarAlterar data={buscarApi.data} realizarBusca={realizarBusca} />
      {message && <Alert severity={type} className="p-3 d-flex gap-3">{message}</Alert>}
      {show? (<FormularioAlterar enviarFormulario={enviarFormulario} data={data} />) : (<p className="d-flex justify-content-center">Selecione um aluno</p>)}
    </Container>
  );
};

export default AlterarNotas;
