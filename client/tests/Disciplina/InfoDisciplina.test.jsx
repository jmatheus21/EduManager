import React from "react";
import { render, screen, waitFor, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { InfoDisciplina } from "../../src/pages/Disciplina";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/disciplina/MAT101",
    search: ""
  }),
  useNavigate: jest.fn(),
  useParams: () => ({
    chave: "MAT101"
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
          codigo: 'MAT101',
          nome: 'Matemática',
          carga_horaria: 60,
          ementa: 'Aritmética e Álgebra',
          bibliografia: 'Matemática - Volume 1, Autor Desconhecido'
        }
    })
}));


describe("InfoDisciplina Component", () => {

    beforeEach(() => {
        render(
            <BrowserRouter>
                <InfoDisciplina />
            </BrowserRouter>
        )
    })

    it ("renderiza todos os componentes na tela", () => { 
               
        // Verifica se o título da página foi renderizado
        expect(screen.getByText(/Informações da Disciplina/i)).toBeVisible();

        // Verifica se o campo referente ao nome foi renderizado
        expect(screen.getByText(/Nome:/i)).toBeVisible();

        // Verifica se o campo referente ao código foi renderizado 
        expect(screen.getByText(/Código:/i)).toBeVisible();

        // Verifica se o campo referente à carga horária foi renderizado
        expect(screen.getByText(/Carga Horária:/i)).toBeVisible();

        // Verifica se o campo referente à ementa foi renderizado
        expect(screen.getByText(/Ementa:/i)).toBeVisible();

        // Verifica se o campo referente à bibliografia foi renderizado
        expect(screen.getByText(/Bibliografia:/i)).toBeVisible();

        // Verifica se o botão 'Alterar' foi renderizado
        expect(screen.getByRole("button", { name: /Alterar/i })).toBeVisible();

        // Verifica se o botão 'Remover' foi renderizado
        expect(screen.getByRole("button", { name: /Remover/i })).toBeVisible();

    });
    

    it("renderiza todos os dados recebidos da API", async () => {

      await waitFor(() => {

        expect(screen.getByText("MAT101")).toBeVisible();
  
        expect(screen.getByText("Matemática")).toBeVisible();

        expect(screen.getByText("60")).toBeVisible();

        expect(screen.getByText("Aritmética e Álgebra")).toBeVisible();

        expect(screen.getByText("Matemática - Volume 1, Autor Desconhecido")).toBeVisible();

      });

    });


    it("abre modal de remover elemento", async () => {
      
      const botaoRemover = screen.getByRole("button", { name: /Remover/i });
      
      await act ( async () => {
        await userEvent.click(botaoRemover);
      });
      
      const modalRemover = screen.getByText(/Remover Disciplina/i);
      expect(modalRemover).toBeVisible();

    });
    
});