import React, { useState } from 'react'
import { Container } from 'react-bootstrap'
import { Alert } from "@mui/material"
import { Titulo } from '../../components'
import Formulario from './components/Formulario'
import useApi from '../../hooks/useApi'

const Matricula = () => {
  const { createData } = useApi("/api");
  const [show, setShow] = useState(false);

  const enviarFormulario = async (data) => {
    try {

      await createData("/aluno/matricula", data)

      setShow(true);

      setTimeout(() => {
        setShow(false)
      }, 5000);

    } catch (e) {
      throw e;
    }
  }

  return (
    <Container fluid>
        <Titulo>Matricular Aluno</Titulo>
        { show && (<Alert severity='success' className="p-2 my-3 d-flex align-content-center gap-3">
          Aluno matriculado com sucesso!
        </Alert>)}
        <Formulario enviarFormulario={enviarFormulario} />
    </Container>
  )
}

export default Matricula