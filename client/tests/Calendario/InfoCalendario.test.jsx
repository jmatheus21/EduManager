import React from "react";
import { render, screen, waitFor, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { InfoCalendario } from "../../src/pages/Calendario";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/calendario/2026",
    search: ""
  }),
  useNavigate: jest.fn(),
  useParams: () => ({
    chave: "2026"
  }),
}));

jest.mock("../../src/hooks/useApi", () => ({
    __esModule: true,
    default: () => ({
        deleteData: jest.fn().mockResolvedValue({ success: true }),
        fetchData: jest.fn().mockResolvedValue({ success: true }),
        loading: false,
        error: null,
        data: {
          ano_letivo: 2026,
          dias_letivos: 150,
          data_inicio: "2026-01-01",
          data_fim: "2026-09-01"
        }
    })
}));


describe("InfoCalendario Component", () => {

    beforeEach(() => {
        render(
            <BrowserRouter>
                <InfoCalendario />
            </BrowserRouter>
        )
    })

    it ("renderiza todos os componentes na tela", () => { 
               
        // Verifica se o título da página foi renderizado
        expect(screen.getByText(/Informações do Calendário/i)).toBeVisible();

        // Verifica se o campo referente ao número foi renderizado
        expect(screen.getByText(/Ano Letivo:/i)).toBeVisible();

        // Verifica se o campo referente à capacidade foi renderizado 
        expect(screen.getByText(/Dias Letivos:/i)).toBeVisible();

        // Verifica se o campo referente à localização foi renderizado
        expect(screen.getByText(/Data de início:/i)).toBeVisible();

        expect(screen.getByText(/Data de fim:/i)).toBeVisible();

        // Verifica se o botão 'Alterar' foi renderizado
        expect(screen.getByRole("button", { name: /Alterar/i })).toBeVisible();

        // Verifica se o botão 'Remover' foi renderizado
        expect(screen.getByRole("button", { name: /Remover/i })).toBeVisible();

    });
    

    it("renderiza todos os dados recebidos da API", async () => {

      await waitFor(() => {

        expect(screen.getByTestId("chave_primaria")).toBeVisible();

        expect(screen.getByText("150")).toBeVisible();

        expect(screen.getByText("01-01-2026")).toBeVisible();

        expect(screen.getByText("01-09-2026")).toBeVisible();

      });

    });


    it("abre modal de remover elemento", async () => {
      
      const botaoRemover = screen.getByRole("button", { name: /Remover/i });
      
      await act ( async () => {
        await userEvent.click(botaoRemover);
      });
      
      const modalRemover = screen.getByText(/Remover Calendário/i);
      expect(modalRemover).toBeVisible();

    });
    
});