import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import  { ConsultarDisciplina } from "../../src/pages/Disciplina"

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useLocation: jest.fn(),
    useNavigate: jest.fn(),
}));

/**
 * Testes unitários para o componente ConsultarDisciplina.
 * Verifica a renderização inicial, a interação do usuário e o carregamento de dados.
 */
describe("ConsultarDisciplina", () => {
    it ("renderiza o formulário corretamente", async () => {
        render(
            <BrowserRouter>
                <ConsultarDisciplina/>
            </BrowserRouter>
        );
        
        // Verifica se o título da página foi renderizado
        expect(await screen.getByText(/Consultar Disciplinas/i)).toBeInTheDocument();

        // Verifica se o campo "Código:" foi renderizado
        expect(screen.getByLabelText(/Código:/i)).toBeInTheDocument();

        // Verifica se o botão foi renderizado
        expect(screen.getByText(/Buscar/i)).toBeInTheDocument();

        // Verifica se o campo "Nome" foi renderizado
        expect(screen.getByText(/Nome/i)).toBeInTheDocument();
        
        // Verifica se o campo "Código" foi renderizado
        expect(screen.getByText(/Código/i)).toBeInTheDocument();

        // Verifica se o campo "Carga Horária" foi renderizado
        expect(screen.getByText(/Carga Horária/i)).toBeInTheDocument();
    });

    it ("exibe a listagem das disciplinas quando os dados forem carregados", async () => {
        render(
            <BrowserRouter>
                <ConsultarDisciplina/>
            </BrowserRouter>
        );
        
        // Simula a resposta da API
        const data = [
            { nome: "Matemática", codigo: "MAT001", carga_horaria: 60},
            { nome: "Português", codigo: "POR001", carga_horaria: 60},
            { nome: "História", codigo: "HIS001", carga_horaria: 60}
        ];    

        // Aguarda a exibição dos dados carregados
        for (const disciplina of data) {
            expect(await screen.findByText(disciplina.nome)).toBeInTheDocument();
            expect(await screen.findByText(disciplina.codigo)).toBeInTheDocument();
            expect(await screen.findByText(String(disciplina.carga_horaria))).toBeInTheDocument();
        }
    });
});