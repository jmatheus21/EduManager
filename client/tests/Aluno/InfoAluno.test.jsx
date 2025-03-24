import React from "react";
import { render, screen, waitFor, act, logRoles } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { InfoAluno } from "../../src/pages/Aluno";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/aluno/202600000001",
    search: ""
  }),
  useNavigate: jest.fn(),
  useParams: () => ({
    chave: "202600000001"
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
          matricula: "202600000001",
          nome: "João Pedro dos Santos",
          email: "joaopedro@email.com",
          telefone: "79 9 1234-5678",
          data_de_nascimento: "2011-09-10",
          endereco: "Bairro X, Rua A",
          turma_id: 1
        }
    })
}));


describe("InfoAluno Component", () => {

    beforeEach(() => {
        render(
            <BrowserRouter>
                <InfoAluno />
            </BrowserRouter>
        )
    })

    it ("renderiza todos os componentes na tela", () => { 
               
        // Verifica se o título da página foi renderizado
        expect(screen.getByText(/Informações do Aluno/i)).toBeVisible();

        // Verifica se o campo referente a matrícula foi renderizado
        expect(screen.getByText(/Matrícula:/i)).toBeVisible();

        // Verifica se o campo referente a turma foi renderizado
        expect(screen.getByText(/Turma:/i)).toBeVisible();

        // Verifica se o campo referente ao nome foi renderizado
        expect(screen.getByText(/Nome:/i)).toBeVisible();

        // Verifica se o campo referente ao email foi renderizado
        expect(screen.getByText(/Email:/i)).toBeVisible();

        // Verifica se o campo referente a data de nascimento foi renderizado
        expect(screen.getByText(/Data de nascimento:/i)).toBeVisible();

        // Verifica se o campo referente ao telefone foi renderizado
        expect(screen.getByText(/Telefone:/i)).toBeVisible();

        // Verifica se o campo referente ao endereço foi renderizado
        expect(screen.getByText(/Endereço:/i)).toBeVisible();

        // Verifica se o botão 'Alterar' foi renderizado
        expect(screen.getByRole("button", { name: /Alterar/i })).toBeVisible();

        // Verifica se o botão 'Remover' foi renderizado
        expect(screen.getByRole("button", { name: /Remover/i })).toBeVisible();

    });
    

    it("renderiza todos os dados recebidos da API", async () => {

      await waitFor(() => {

        expect(screen.getByText("202600000001")).toBeVisible();

        expect(screen.getByText("João Pedro dos Santos")).toBeVisible();

        expect(screen.getByText("joaopedro@email.com")).toBeVisible();

        expect(screen.getByText("79 9 1234-5678")).toBeVisible();

        expect(screen.getByText("2011-09-10")).toBeVisible();

        expect(screen.getByText("Bairro X, Rua A")).toBeVisible();
        
        expect(screen.getByTestId("turma_id")).toBeVisible();
        
      });
      
      
    });

    it("abre modal de remover elemento", async () => {
      
      const botaoRemover = screen.getByRole("button", { name: /Remover/i });
      
      await act ( async () => {
        await userEvent.click(botaoRemover);
      });
      
      const modalRemover = screen.getByText(/Remover Aluno/i);
      expect(modalRemover).toBeVisible();

    });

});