import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import  { ConsultarTurma } from "../../src/pages/Turma"

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useLocation: jest.fn(),
    useNavigate: jest.fn(),
}));

/**
 * Testes unitários para o componente ConsultarTurma.
 * Verifica a renderização inicial, a interação do usuário e o carregamento de dados.
 */
describe("ConsultarTurma", () => {
    it ("renderiza o formulário corretamente", async () => {
        render(
            <BrowserRouter>
                <ConsultarTurma/>
            </BrowserRouter>
        );
        
        // Verifica se o título da página foi renderizado
        expect(await screen.getByText(/Consultar Turmas/i)).toBeInTheDocument();

        // Verifica se o campo "Id da turma:" foi renderizado
        expect(screen.getByLabelText(/Id da turma:/i)).toBeInTheDocument();

        // Verifica se o botão foi renderizado
        expect(screen.getByText(/Buscar/i)).toBeInTheDocument();

        // Verifica se o campo "Id" foi renderizado
        expect(screen.getByText(/Id/i)).toBeInTheDocument();

        // Verifica se o campo "Ano Letivo" foi renderizado
        expect(screen.getByText(/Ano Letivo/i)).toBeInTheDocument();

        // Verifica se o campo "Ano" foi renderizado
        expect(screen.getByText(/Ano/i)).toBeInTheDocument();

        // Verifica se o campo "Série" foi renderizado
        expect(screen.getByText(/Série/i)).toBeInTheDocument();

        // Verifica se o campo "Nível de Ensino" foi renderizado
        expect(screen.getByText(/Nível de Ensino/i)).toBeInTheDocument();

        // Verifica se o campo "Turno" foi renderizado
        expect(screen.getByText(/Turno/i)).toBeInTheDocument();

        // Verifica se o campo "Status" foi renderizado
        expect(screen.getByText(/Status/i)).toBeInTheDocument();

    });

    // it ("exibe a listagem das turmas quando os dados forem carregados", async () => {
    //     render(
    //         <BrowserRouter>
    //             <ConsultarTurma/>
    //         </BrowserRouter>
    //     );
        
    //     // Simula a resposta da API
    //     const data = [
    //         { ano_letivo: 2026, ano: 1, serie: "A", nivel_de_ensino: "Ensino Médio", turno: "V", status: "A"},
    //         { ano_letivo: 2026, ano: 4, serie: "C", nivel_de_ensino: "Ensino Fundamental", turno: "D", status: "C"},
    //         { ano_letivo: 2027, ano: 9, serie: "B", nivel_de_ensino: "Ensino Fundamental", turno: "N", status: "C"}
    //     ];    

    //     // Aguarda a exibição dos dados carregados
    //     for (const turma of data) {
    //         expect(await screen.findByText(turma.id.toString())).toBeInTheDocument();
    //         expect(await screen.findByText(turma.calendario_ano_letivo.toString())).toBeInTheDocument();
    //         expect(await screen.findByText(turma.ano.toString())).toBeInTheDocument();
    //         expect(await screen.findByText(turma.serie)).toBeInTheDocument();
    //         expect(await screen.findByText(turma.nivel_de_ensino)).toBeInTheDocument();
    //         expect(await screen.findByText(turma.turno)).toBeInTheDocument();
    //         expect(await screen.findByText(turma.status)).toBeInTheDocument();
    //     }
    // });
});