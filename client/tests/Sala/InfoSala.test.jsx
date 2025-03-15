import React from "react";
import { render, screen, waitFor, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { InfoSala } from "../../src/pages/Sala";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/sala/1",
    search: ""
  }),
  useNavigate: jest.fn(),
  useParams: () => ({
    chave: "1"
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
          numero: 123,
          capacidade: 100,
          localizacao: "Bloco A, 1° andar"
        }
    })
}));


describe("InfoSala Component", () => {

    beforeEach(() => {
        render(
            <BrowserRouter>
                <InfoSala />
            </BrowserRouter>
        )
    })

    it ("renderiza todos os componentes na tela", () => { 
               
        // Verifica se o título da página foi renderizado
        expect(screen.getByText(/Informações da Sala/i)).toBeVisible();

        // Verifica se o campo referente ao número foi renderizado
        expect(screen.getByText(/Número:/i)).toBeVisible();

        // Verifica se o campo referente à capacidade foi renderizado 
        expect(screen.getByText(/Capacidade:/i)).toBeVisible();

        // Verifica se o campo referente à localização foi renderizado
        expect(screen.getByText(/Localização:/i)).toBeVisible();

        // Verifica se o botão 'Alterar' foi renderizado
        expect(screen.getByRole("button", { name: /Alterar/i })).toBeVisible();

        // Verifica se o botão 'Remover' foi renderizado
        expect(screen.getByRole("button", { name: /Remover/i })).toBeVisible();

    });
    

    it("renderiza todos os dados recebidos da API", async () => {

      await waitFor(() => {

        expect(screen.getByText("123")).toBeVisible();
  
        expect(screen.getByText("100")).toBeVisible();

        expect(screen.getByText("Bloco A, 1° andar")).toBeVisible();

      });

    });


    it("abre modal de remover elemento", async () => {
      
      const botaoRemover = screen.getByRole("button", { name: /Remover/i });
      
      await act ( async () => {
        await userEvent.click(botaoRemover);
      });
      
      const modalRemover = screen.getByText(/Remover Sala/i);
      expect(modalRemover).toBeVisible();

    });
    
});