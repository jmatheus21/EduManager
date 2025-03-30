import React from "react";
import { useForm } from "react-hook-form";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import Paper from '@mui/material/Paper';
import { Form } from "react-bootstrap"
import { Botao } from "../../../components/Botao";

export default function Formulario({ alunos = [], enviarFormulario }) {
  const { register, handleSubmit } = useForm();

  const handleSave = async (data) => {
    const formattedData = {
      alunos: Object.entries(data).map(([matricula, ausencia]) => ({
        matricula: matricula,
        ausencia: ausencia || false
      }))
    };
    
    try {
      await enviarFormulario(formattedData)
    } catch (e) {
      console.error("Erro: " + e.message)
    }
  }

  return (
    <form onSubmit={handleSubmit(handleSave)} className="w-100">
      <TableContainer component={Paper} className="my-3">
        <Table sx={{ minWidth: "500px" }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell sx={{ width: '30%' }} className="p-2 fw-bold fs-5">Matrícula</TableCell>
              <TableCell sx={{ width: '50%' }} className="p-2 fw-bold fs-5">Nome</TableCell>
              <TableCell sx={{ width: '20%' }} className="p-2 fw-bold fs-5">Ausência</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {
              alunos.map((item) => (
                <TableRow
                  key={item.matricula}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell className="p-2">{item.matricula}</TableCell>
                  <TableCell className="p-2">{item.nome}</TableCell>
                  <TableCell className="p-2">
                    <Form.Check
                        type="checkbox"
                        id={`ausencia-${item.matricula}`}
                        label={<span className="visually-hidden">{item.nome}</span>}
                        {...register(`${item.matricula}`, { required: false })}
                    />
                  </TableCell>
                </TableRow>
              ))
            }
          </TableBody>
        </Table>
      </TableContainer>
      <Botao.Group>
        <Botao.Base title={"Salvar"} type="submit" />
      </Botao.Group>
    </form>
  );
}