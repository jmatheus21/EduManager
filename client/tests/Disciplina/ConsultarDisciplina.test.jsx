import React from "react";
import { render, screen, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import  { ConsultarDisciplina } from "../../src/pages/Disciplina"

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useLocation: () => ({
        pathname: "/disciplina"
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
 * Testes unitários para o componente ConsultarDisciplina.
 * Verifica a renderização inicial, a interação do usuário e o carregamento de dados.
 */
describe("ConsultarDisciplina", () => {

    beforeEach(() => {
        render(
            <BrowserRouter>
                <ConsultarDisciplina/>
            </BrowserRouter>
        );
    })

    it("renderiza o formulário corretamente", async () => {
        
        // Verifica se o título da página foi renderizado
        expect(await screen.getByText(/Consultar Disciplinas/i)).toBeVisible();

        // // Verifica se o campo "Código:" foi renderizado
        expect(screen.getByPlaceholderText("Exemplo: MAT001")).toBeVisible();

        // // Verifica se o botão foi renderizado
        expect(screen.getByText(/Buscar/i)).toBeVisible();

        // // Verifica se o campo "Nome" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Nome/i })).toBeVisible();   
        
        // // Verifica se o campo "Código" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Código/i })).toBeVisible();

        // // Verifica se o campo "Carga Horária" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Carga Horária/i })).toBeVisible();
    });

    it("verifica se é possível inserir dados no campo de busca", async () => {
        render(
            <BrowserRouter>
                <ConsultarDisciplina/>
            </BrowserRouter>
        );

        const camposBusca = screen.getAllByPlaceholderText("Exemplo: MAT001");
        const campoBusca = camposBusca[0];

        await act( async () => {
            await userEvent.type(campoBusca, "MAT101");
        });

        expect(campoBusca.value).toBe("MAT101");
    });
});