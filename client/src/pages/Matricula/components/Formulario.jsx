import React, { useState } from 'react'
import { Alert, Container, Form } from 'react-bootstrap'
import { useForm } from 'react-hook-form'
import BotaoSpinner from '../../../components/BotaoSpinner'

const Formulario = ({ enviarFormulario }) => {
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [loading, setLoading] = useState(false);

    const onSubmit = async (data) => {

        setLoading(true)

        try {

            await enviarFormulario(data);
            
        } catch(e) {
            console.error(e);
        } finally {
            setLoading(false)
        }
    }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
        <Container fluid className='my-3 d-grid gap-3'>
            <Form.Group className="d-flex flex-column gap-1">
                <Form.Label htmlFor='matricula'>Matrícula do aluno:</Form.Label>
                <Form.Control
                    id="matricula"
                    type='text'
                    className='p-2'
                    placeholder='Exemplo: 202500001223'
                    {...register("aluno_matricula", { required: true, minLength: 12, maxLength: 12 })}
                />
                <Alert variant='white' className={`${errors.aluno_matricula? "" : "d-none"} py-2 text-danger`}>
                    { errors.aluno_matricula?.type == "required" && "A matrícula do aluno é obrigatória"}
                    { (errors.aluno_matricula?.type == "minLength" ||  errors.aluno_matricula?.type == "maxLength") && "A matrícula do aluno deve ter exatamente 12 caracteres"}
                </Alert>
            </Form.Group>
            <Form.Group className="d-flex flex-column gap-1">
                <Form.Label htmlFor='id-turma'>Id da turma:</Form.Label>
                <Form.Control
                    id='id-turma'
                    type='number'
                    className='p-2'
                    placeholder='Exemplo: 1230'
                    {...register("turma_id", { required: true, min: 1, valueAsNumber: true})}
                />
                <Alert variant='white' className={`${errors.turma_id? "" : "d-none"} py-2 text-danger`}>
                    { errors.turma_id?.type == "required" && "O id da turma é obrigatório"}
                    { errors.matricula?.type == "min" && "O id da turma não pode ser menor que 1"}
                </Alert>
            </Form.Group>
            <BotaoSpinner loading={loading} fixo={"Matricular"} temp={"Matriculando..."} />
        </Container>
    </Form>
  )
}

export default Formulario