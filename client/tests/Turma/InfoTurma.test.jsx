import React from "react";
import { render, screen, waitFor, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { InfoTurma } from "../../src/pages/Turma";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/turma/1",
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
            id: 1,
            ano: 9,
            serie: "D",
            nivel_de_ensino: "Ensino Fundamental",
            turno: "N",
            status: "A",
            sala_numero: 101,
            calendario_ano_letivo: 2026
        }
    })
}));


describe("InfoTurma Component", () => {

    beforeEach(() => {
        render(
            <BrowserRouter>
                <InfoTurma />
            </BrowserRouter>
        )
    })

    it ("renderiza todos os componentes na tela", () => { 
               
        // Verifica se o título da página foi renderizado
        expect(screen.getByText(/Informações da Turma/i)).toBeVisible();

        // Verifica se o campo referente ao id foi renderizado
        expect(screen.getByText(/Identificação:/i)).toBeVisible();

        // Verifica se o campo referente ao ano letivo do calendario foi renderizado 
        expect(screen.getByText(/Ano letivo:/i)).toBeVisible();

        // Verifica se o campo referente ao ano foi renderizado
        expect(screen.getByText(/Ano:/i)).toBeVisible();

        // Verifica se o campo referente à série foi renderizado
        expect(screen.getByText(/Série:/i)).toBeVisible();

        // Verifica se o campo referente ao nível de ensino foi renderizado
        expect(screen.getByText(/Nível de Ensino:/i)).toBeVisible();

        // Verifica se o campo referente ao turno foi renderizado
        expect(screen.getByText(/Turno:/i)).toBeVisible();

        // Verifica se o campo referente ao status foi renderizado
        expect(screen.getByText(/Status:/i)).toBeVisible();

        // Verifica se o campo referente à sala foi renderizado
        expect(screen.getByText(/Sala:/i)).toBeVisible();

        // Verifica se o botão 'Alterar' foi renderizado
        expect(screen.getByRole("button", { name: /Alterar/i })).toBeVisible();

        // Verifica se o botão 'Remover' foi renderizado
        expect(screen.getByRole("button", { name: /Remover/i })).toBeVisible();

    });
    

    it("renderiza todos os dados recebidos da API", async () => {

      await waitFor(() => {

        expect(screen.getByTestId("chave_primaria")).toBeVisible();

        expect(screen.getByText("9")).toBeVisible();

        expect(screen.getByText("D")).toBeVisible();

        expect(screen.getByText("Ensino Fundamental")).toBeVisible();

        expect(screen.getByText("Noturno")).toBeVisible();
        
        expect(screen.getByText("Ativa")).toBeVisible();

        expect(screen.getByText("101")).toBeVisible();

        expect(screen.getByText("2026")).toBeVisible();    
        
      });

    });


    it("abre modal de remover elemento", async () => {
      
      const botaoRemover = screen.getByRole("button", { name: /Remover/i });
      
      await act ( async () => {
        await userEvent.click(botaoRemover);
      });
      
      const modalRemover = screen.getByText(/Remover Turma/i);
      expect(modalRemover).toBeVisible();

    });

});