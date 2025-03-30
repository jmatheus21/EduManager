import React from 'react'
import { Container, Form } from 'react-bootstrap'
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead } from '@mui/material'
import { useForm } from 'react-hook-form';
import { Botao } from '../../../components/Botao';

const exibirSituacao = (situacao) => {
    switch (situacao) {
        case "A":
            return "APROVADO";
        case "R":
            return "REPROVADO";
        default:
            return "MATRICULADO";
    }
}

const media = (array) => {
    const soma = array.reduce((acc, v) => acc + v, 0);
    const media = soma / 4
    return media.toFixed(1)
}

const FormularioAlterar = ({ data, enviarFormulario }) => {
    const { register, handleSubmit } = useForm()

    const onSubmit = async (dados) => {
        
        dados = { notas: [ parseFloat(dados.u1) || 0.0, parseFloat(dados.u2) || 0.0, parseFloat(dados.u3) || 0.0, parseFloat(dados.u4) || 0.0 ]}

        try {
            await enviarFormulario(dados);
        } catch(e) {
            console.error(e)
        }
    }

  return (
    <Container fluid className="mt-5">
      {data && console.log(data)}
      <Form onSubmit={handleSubmit(onSubmit)}>
          <p>
            <strong>Nome: </strong> {data?.nome}
          </p>
          <TableContainer component={Paper} className="my-3">
            <Table>
              <TableHead>
                <TableCell className="p-2 fw-bold text-center">
                  <Form.Label htmlFor='unid1'>1° Unidade</Form.Label>
                </TableCell>
                <TableCell className="p-2 fw-bold text-center">
                  <Form.Label htmlFor='unid2'>2° Unidade</Form.Label>
                </TableCell>
                <TableCell className="p-2 fw-bold text-center">
                  <Form.Label htmlFor='unid3'>3° Unidade</Form.Label>
                </TableCell>
                <TableCell className="p-2 fw-bold text-center">
                  <Form.Label htmlFor='unid4'>4° Unidade</Form.Label>
                </TableCell>
                <TableCell className="p-2 fw-bold text-center">
                  Média Final
                </TableCell>
                <TableCell className="p-2 fw-bold text-center">Situação</TableCell>
              </TableHead>
              <TableBody>
                <TableCell className="p-2 text-center">{data?.notas[0]? (
                    <Form.Control
                        id='unid1'
                        type="number"
                        step="0.1"
                        min="0"
                        max="10"
                        className='p-1 text-center'
                        {...register("u1", { required: false, valueAsNumber: true, min: 0.0, max: 10.0 })}
                        defaultValue={data.notas[0]}
                    />
                ) : "---"}</TableCell>
                <TableCell className="p-2 text-center">{data?.notas[1]? (
                    <Form.Control
                        id='unid2'
                        type="number"
                        step="0.1"
                        min="0"
                        max="10"
                        className='p-1 text-center'
                        {...register("u2", { required: false, valueAsNumber: true, min: 0.0, max: 10.0 })}
                        defaultValue={data.notas[1]}
                    />
                ) : "---"}</TableCell>
                <TableCell className="p-2 text-center">{data?.notas[2]? (
                    <Form.Control
                        id='unid3'
                        type="number"
                        step="0.1"
                        min="0"
                        max="10"
                        className='p-1 text-center'
                        {...register("u3", { required: false, valueAsNumber: true, min: 0.0, max: 10.0 })}
                        defaultValue={data.notas[2]}
                    />
                ) : "---"}</TableCell>
                <TableCell className="p-2 text-center">{data?.notas[3]? (
                    <Form.Control
                        id='unid4'
                        type="number"
                        step="0.1"
                        min="0"
                        max="10"
                        className='p-1 text-center'
                        {...register("u4", { required: false, valueAsNumber: true, min: 0.0, max: 10.0 })}
                        defaultValue={data.notas[3]}
                    />
                ) : "---"}</TableCell>
                <TableCell className="p-2 text-center">{data?.notas && data.notas.length == 4? media(data.notas) : "---"}</TableCell>
                <TableCell className="p-2 text-center">{exibirSituacao(data?.situacao)}</TableCell>
              </TableBody>
            </Table>
          </TableContainer>
          <Botao.Group>
            <Botao.Base title="Salvar" type="submit" />
          </Botao.Group>
      </Form>
    </Container>
  );
};

export default FormularioAlterar;
