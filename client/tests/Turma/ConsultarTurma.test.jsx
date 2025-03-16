import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import  { ConsultarTurma } from "../../src/pages/Turma"

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useLocation: () => ({
        pathname: "/turma/consultar",
        search: "?sucess=true",
    }),
    useNavigate: jest.fn(),
}));

jest.mock("../../src/hooks/useApi", () => ({
    __esModule: true,
    default: () => ({
        fetchData: jest.fn().mockResolvedValue({ success: true }),
        loading: false,
        error: null,
        data: []
    })
}));


/**
 * Testes unitários para o componente ConsultarTurma.
 * Verifica a renderização inicial, a interação do usuário e o carregamento de dados.
 */
describe("ConsultarTurma", () => {
    it ("renderiza a página corretamente", async () => {
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

        // Verifica se o campo "Ano" aparece duas vezes em "Ano Letivo" e em "Ano"
        const anoHeading = screen.getAllByText(/Ano/i);
        expect(anoHeading.length).toBe(2);

        // Verifica se o campo "Série" foi renderizado
        expect(screen.getByText(/Série/i)).toBeInTheDocument();

        // Verifica se o campo "Nível de Ensino" foi renderizado
        expect(screen.getByText(/Nível de Ensino/i)).toBeInTheDocument();

        // Verifica se o campo "Turno" foi renderizado
        expect(screen.getByText(/Turno/i)).toBeInTheDocument();

        // Verifica se o campo "Status" foi renderizado
        expect(screen.getByText(/Status/i)).toBeInTheDocument();

    });

    it("verifica se é possível inserir dados no campo de busca", async () => {
        render(
            <BrowserRouter>
                <ConsultarTurma/>
            </BrowserRouter>
        );

        const campoBusca = screen.getByLabelText(/Id da turma:/i);

        await userEvent.type(campoBusca, "1");

        expect(campoBusca.value).toBe("1");
    });

});