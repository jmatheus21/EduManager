import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { ConsultarAula } from "../../src/pages/Aula"

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useLocation: () => ({
        pathname: "/aula/consultar",
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
 * Testes unitários para o componente ConsultarAula.
 * Verifica a renderização inicial, a interação do usuário e o carregamento de dados.
 */
describe("ConsultarAula", () => {
    it("renderiza a página corretamente", async () => {
        render(
            <BrowserRouter>
                <ConsultarAula />
            </BrowserRouter>
        );

        // Verifica se o título da página foi renderizado
        expect(await screen.getByText(/Consultar Aulas/i)).toBeInTheDocument();

        // Verifica se o campo "Id da turma:" foi renderizado
        expect(screen.getByLabelText(/Id da aula:/i)).toBeInTheDocument();

        // Verifica se o botão foi renderizado
        expect(screen.getByText(/Buscar/i)).toBeInTheDocument();

        // Verifica se o campo "#" foi renderizado
        expect(screen.getByText(/#/i)).toBeInTheDocument();

        // Verifica se o campo "Turma" foi renderizado
        expect(screen.getByText(/Turma/i)).toBeInTheDocument();

        // Verifica se o campo "Disciplina" foi renderizado
        expect(screen.getByText(/Disciplina/i)).toBeInTheDocument();

        // Verifica se o campo "Professor" foi renderizado
        expect(screen.getByText(/Professor/i)).toBeInTheDocument();

        // Verifica se o campo "H.Início" foi renderizado
        expect(screen.getByText(/H.Início/i)).toBeInTheDocument();

        // Verifica se o campo "H.Fim" foi renderizado
        expect(screen.getByText(/H.Fim/i)).toBeInTheDocument();

        // Verifica se o campo "Dias da Semana" foi renderizado
        expect(screen.getByText(/Dias da Semana/i)).toBeInTheDocument();

    });

    it("verifica se é possível inserir dados no campo de busca", async () => {
        render(
            <BrowserRouter>
                <ConsultarAula />
            </BrowserRouter>
        );

        const campoBusca = screen.getByLabelText(/Id da aula:/i);

        await userEvent.type(campoBusca, "1");

        expect(campoBusca.value).toBe("1");
    });

});