import React from "react";
import { render, screen, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import  { ConsultarCalendario } from "../../src/pages/Calendario"

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useLocation: () => ({
        pathname: "/calendario"
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
 * Testes unitários para o componente ConsultarCalendario.
 * Verifica a renderização inicial, a interação do usuário e o carregamento de dados.
 */
describe("ConsultarCalendario", () => {

    beforeEach(() => {
        render(
            <BrowserRouter>
                <ConsultarCalendario/>
            </BrowserRouter>
        );
    })

    it ("renderiza o formulário corretamente", async () => {
        
        // Verifica se o título da página foi renderizado
        expect(await screen.getByText(/Consultar Calendários/i)).toBeVisible();

        // // Verifica se o campo "Ano letivo:" foi renderizado
        expect(screen.getByLabelText(/Ano letivo:/i)).toBeVisible();

        // // Verifica se o botão foi renderizado
        expect(screen.getByText(/Buscar/i)).toBeVisible();

        // // Verifica se o campo "Ano letivo" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Ano letivo/i })).toBeVisible();   
        
        // // Verifica se o campo "Dias Letivos" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Dias Letivos/i })).toBeVisible();

        // // Verifica se o campo "Data de início" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Data de início/i })).toBeVisible();

        // // Verifica se o campo "Data de fim" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Data de fim/i })).toBeVisible();
    });

    it ("verifica se é possível inserir dados no campo de busca", async () => {
        render(
            <BrowserRouter>
                <ConsultarCalendario/>
            </BrowserRouter>
        );

        const campoBusca = screen.getByLabelText(/Ano letivo:/i);

        await act( async () => {
            await userEvent.type(campoBusca, "2026");
        });

        expect(campoBusca.value).toBe("2026");
    });
});