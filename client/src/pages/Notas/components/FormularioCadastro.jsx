import React from "react";
import { useForm } from "react-hook-form";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import Paper from '@mui/material/Paper';
import { Form } from "react-bootstrap"
import { Botao } from "../../../components/Botao";

export default function FormularioCadastro({ alunos = [], enviarFormulario }) {
  const { register, handleSubmit } = useForm();

  const handleSave = async (data) => {
    const formattedData = {
      alunos: Object.entries(data).map(([matricula, nota]) => ({
        matricula: matricula,
        nota: parseFloat(nota) || 5.0
      }))
    };
    
    try {
      await enviarFormulario(formattedData)
    } catch (e) {
      console.error(e)
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
              <TableCell sx={{ width: '20%' }} className="p-2 fw-bold fs-5">Nota</TableCell>
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
                  <TableCell className="p-2"><Form.Label htmlFor={item.matricula}>{item.nome}</Form.Label></TableCell>
                  <TableCell className="p-2">
                    <Form.Control
                      id={item.matricula}
                      type="number"
                      step="0.1"
                      min="0"
                      max="10"
                      {...register(`${item.matricula}`, { required: true, min: 0.0, max: 10.0 })}
                      defaultValue=""
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