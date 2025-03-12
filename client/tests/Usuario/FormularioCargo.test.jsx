import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { FormularioCargo } from "../../src/pages/Cargo";
import { useForm } from 'react-hook-form';

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: jest.fn(),
  useNavigate: jest.fn(),
}));

// Mock do useForm
jest.mock('react-hook-form', () => ({
    ...jest.requireActual('react-hook-form'),
    useForm: () => ({
        register: jest.fn(),
        handleSubmit: jest.fn((fn) => fn),
        reset: jest.fn(),
        formState: { errors: {} },
    }),
}));

describe("ConsultarCargo Component", () => {
    const mockFields = [];
    const mockAppend = jest.fn();
    const mockRemove = jest.fn();
    const mockErro = {};

    it("renderiza formulário corretamente", () => {

        render (
            <BrowserRouter>
                <FormularioCargo
                    fields={mockFields}
                    append={mockAppend}
                    remove={mockRemove}
                    erro={mockErro}
                />
            </BrowserRouter>
        )

        expect(screen.getByText(/Cargos/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Nome:/i)).toBeInTheDocument();
        expect(screen.getByTestId('salarioCargo')).toBeInTheDocument();
        expect(screen.getByLabelText(/Data de contrato:/i)).toBeInTheDocument();
        expect(screen.getByText("Adicionar")).toBeInTheDocument();    

    })

    it("permite ao usuário digitar nos campos", () => {

        render (
            <BrowserRouter>
                <FormularioCargo
                    fields={mockFields}
                    append={mockAppend}
                    remove={mockRemove}
                    erro={mockErro}
                />
            </BrowserRouter>
        )

        const nomeInput = screen.getByLabelText(/Nome:/i);
        fireEvent.change(nomeInput, { target: { value: 'Professor' } });
        
        const salarioInput = screen.getByTestId('salarioCargoInput');
        fireEvent.change(salarioInput, { target: {value: 3040.5}});

        const dataDeContratoInput = screen.getByLabelText(/Data de contrato:/i);
        fireEvent.change(dataDeContratoInput, { target: {value: '2030-01-01'}});

        expect(nomeInput.value).toBe('Professor');
        expect(salarioInput.value).toBe("3040.5");
        expect(dataDeContratoInput.value).toBe("2030-01-01");

    })
})