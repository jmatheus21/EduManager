import React from 'react'
import { Row, Col, Form, Button, Container, Alert, Table } from "react-bootstrap";
import { useForm } from "react-hook-form";
import { isDate, isAfter } from "validator";
import { FaTrash } from "react-icons/fa";
import { inverterData } from "../../components/Listagem"

const data = new Date();
const dia = data.getDate() < 10 ? "0" + data.getDate() : data.getDate();
const mes = (data.getMonth() + 1) < 10 ? "0" + (data.getMonth() + 1) : (data.getMonth() + 1);
const hoje = `${data.getFullYear()}-${mes}-${dia}`;

export const formatarMoeda = (valor) => {
    return valor.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL',
    });
};

const FormularioCargo = ({ fields, append, remove, erro, setError, clearErrors }) => {
    const { register, handleSubmit, reset, formState: { errors } } = useForm();

    const adicionarCargo = (data) => {
        const cargoExistente = fields.find(cargo => cargo.nome === data.nome);

        if (cargoExistente) {
            setError("cargos", { type: "equal" });
            reset({ 
                nome: "",
                salario: "",
                data_contrato: ""
            });
            return;
        }
        
        append({
            nome: data.nome,
            salario: parseFloat(data.salario) || 0.0,
            data_contrato: data.data_contrato
        });
        
        reset({
            nome: "",
            salario: "",
            data_contrato: ""
        });
        
        clearErrors("cargos");
    };

  return (
    <fieldset className="border rounded-3 p-3">
        <legend className="float-none w-auto px-1 fs-6">Cargos</legend>
            <Row className='gap-3'>
                <Col>
                    <Form.Group className="d-flex flex-column gap-1">
                        <Form.Label htmlFor="nomeCargo" data-testid="nomeCargo">Nome: <span className="text-danger">*</span></Form.Label>
                            <Form.Control
                                id="nomeCargo"
                                type="text"
                                className="p-2"
                                placeholder="Administrador de Recursos"
                                {...register("nome", { required: true, minLength: 5, maxLength: 100 })}
                            />
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="d-flex flex-column gap-1">
                        <Form.Label htmlFor="salarioCargo" data-testid="salarioCargo">Salário Mensal (R$): <span className="text-danger">*</span></Form.Label>
                            <Form.Control
                                id="salarioCargo"
                                type="number"
                                className="p-2"
                                step="10.00"
                                placeholder='3040,00'
                                data-testid="salarioCargoInput"
                                {...register("salario", { required: true, min: 100.0, max: 999999999.0 })}
                            />
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="d-flex flex-column gap-1">
                        <Form.Label htmlFor="dataContratoCargo" data-testid="dataContratoCargo">Data de contrato: <span className="text-danger">*</span></Form.Label>
                            <Form.Control
                                id="dataContratoCargo"
                                type="date"
                                className="p-2"
                                data-testid="dataContratoCargoControl"
                                {...register("data_contrato", { required: true, validate: (value) => isDate(value) && isAfter(value, hoje) })}
                            />
                    </Form.Group>
                </Col>
                <Col className='d-flex align-items-end justify-content-end'>
                    <Button
                        variant="primary"
                        type="submit"
                        className="py-2 px-3"
                        onClick={handleSubmit(adicionarCargo)}
                    >
                        Adicionar
                    </Button>
                </Col>
            </Row>
            <Row>
                <Alert variant="white" className={`${errors? "d-flex" : "d-none"} text-danger justify-content-center pb-1 pt-2`}>
                    {erro?.cargos?.type == "void" && "Nenhum cargo foi cadastrado"}
                    {erro?.cargos?.type == "equal" && "Este cargo já foi adicionado!"}
                    {errors?.nome?.type == "required" && "O nome do cargo é obrigatório"}
                    {errors?.salario?.type == "required" && "O salário é obrigatório"}
                    {errors?.salario?.type == "min" && "O salário deve ser maior que R$ 100"}
                    {errors?.salario?.type == "max" && "O salário deve ser menor que R$ 999999999"}
                    {errors?.data_contrato?.type == "required" && "A data de contrato é obrigatória"}
                    {errors?.data_contrato?.type == "validate" && "A data de contrato deve ser uma data futura"}
                </Alert>
            </Row>
        <Container fluid className="mt-3">
            <Table>
                <thead>
                    <tr>
                        <th className='py-2'>Nome</th>
                        <th className='py-2 text-center'>Salário mensal</th>
                        <th className='py-2 text-center'>Data de contrato</th>
                        <th className='py-2 text-center'>Remover</th>
                    </tr>
                </thead>
                <tbody>        
                    {
                        fields.map((item, index) => (
                            <tr key={index}>
                                <td className='py-2'>{item.nome}</td>
                                <td className='py-2 text-center'>{formatarMoeda(item.salario)}</td>
                                <td className='py-2 text-center'>{inverterData(item.data_contrato)}</td>
                                <td className='py-2 text-center'><button className='border-0' onClick={()=>remove(index)}><FaTrash size={20} /></button></td>
                            </tr>
                        ))
                    }
                </tbody>
            </Table>
        </Container>
    </fieldset>
  )
}

export default FormularioCargo