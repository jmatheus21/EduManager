import React from "react";
import { render, screen, fireEvent, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import  { ConsultarSala } from "../../src/pages/Sala"
import useApi from "../../src/hooks/useApi";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useLocation: () => ({
        pathname: "/sala"
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
 * Testes unitários para o componente ConsultarSala.
 * Verifica a renderização inicial, a interação do usuário e o carregamento de dados.
 */
describe("ConsultarSala", () => {

    beforeEach(() => {
        render(
            <BrowserRouter>
                <ConsultarSala/>
            </BrowserRouter>
        );
    })

    it("renderiza o formulário corretamente", async () => {
        
        // Verifica se o título da página foi renderizado
        expect(await screen.getByText(/Consultar Salas/i)).toBeVisible();

        // // Verifica se o campo "Número:" foi renderizado
        expect(screen.getByLabelText(/Número:/i)).toBeVisible();

        // // Verifica se o botão foi renderizado
        expect(screen.getByText(/Buscar/i)).toBeVisible();

        // // Verifica se o campo "Número" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Número/i })).toBeVisible();   
        
        // // Verifica se o campo "Capacidade" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Capacidade/i })).toBeVisible();

        // // Verifica se o campo "Localização" foi renderizado
        expect(screen.getByRole("columnheader", { name: /Localização/i })).toBeVisible();
    });

    it("verifica se é possível inserir dados no campo de busca", async () => {
        render(
            <BrowserRouter>
                <ConsultarSala/>
            </BrowserRouter>
        );

        const campoBusca = screen.getByLabelText(/Número:/i);

        await act( async () => {
            await userEvent.type(campoBusca, "123");
        });

        expect(campoBusca.value).toBe("123");
    });
});