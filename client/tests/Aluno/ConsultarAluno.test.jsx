import React from "react";
import { render, screen, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { ConsultarAluno } from "../../src/pages/Aluno"

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useLocation: () => ({
        pathname: "/aluno/consultar",
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
 * Testes unitários para o componente ConsultarAluno.
 * Verifica a renderização inicial, a interação do usuário e o carregamento de dados.
 */
describe("ConsultarAluno", () => {
    it("renderiza a página corretamente", async () => {
        render(
            <BrowserRouter>
                <ConsultarAluno />
            </BrowserRouter>
        );

        // Verifica se o título da página foi renderizado
        expect(await screen.getByText(/Consultar Alunos/i)).toBeInTheDocument();

        // Verifica se o campo "Matrícula:" foi renderizado
        expect(screen.getByPlaceholderText("Exemplo: 202600000001")).toBeInTheDocument();

        // Verifica se o botão foi renderizado
        expect(screen.getByText(/Buscar/i)).toBeInTheDocument();

        // Verifica se o campo "Matrícula" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Matrícula/i })).toBeVisible();

        // Verifica se o campo "Nome" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Nome/i })).toBeVisible();

        // Verifica se o campo "Turma" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Turma/i })).toBeVisible();

        // Verifica se o campo "E-mail" foi renderizado
        expect(screen.getByRole("columnheader", { name: /E-mail/i })).toBeVisible();

        // Verifica se o campo "Telefone" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Telefone/i })).toBeVisible();

        // Verifica se o campo "Data de Nascimento" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Data de Nascimento/i })).toBeVisible(); 
    });


    it ("verifica se é possível inserir dados no campo de busca", async () => {
        render(
            <BrowserRouter>
                <ConsultarAluno/>
            </BrowserRouter>
        );

        const camposBusca = screen.getAllByPlaceholderText("Exemplo: 202600000001");
        const campoBusca = camposBusca[0];

        await act( async () => {
            await userEvent.type(campoBusca, "202600000001");
        });

        expect(campoBusca.value).toBe("202600000001");
    });
});
