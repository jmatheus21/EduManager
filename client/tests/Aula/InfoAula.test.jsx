import React from "react";
import { render, screen, waitFor, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { InfoAula } from "../../src/pages/Aula";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/aula/1",
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
            turma_id: 1,
            professor_nome: "João Paulo Silva",
            disciplina_codigo: "MAT001",
            hora_inicio: "07:00",
            hora_fim: "09:00",
            dias_da_semana: "Segunda e Quarta"
        }
    })
}));


describe("InfoAula Component", () => {

    beforeEach(() => {
        render(
            <BrowserRouter>
                <InfoAula />
            </BrowserRouter>
        )
    })

    it ("renderiza todos os componentes na tela", () => { 
               
        // Verifica se o título da página foi renderizado
        expect(screen.getByText(/Informações da Aula/i)).toBeVisible();

        // Verifica se o campo referente ao id foi renderizado
        expect(screen.getByText(/Identificação:/i)).toBeVisible();

        // Verifica se o campo referente a turma foi renderizado 
        expect(screen.getByText(/Turma:/i)).toBeVisible();

        // Verifica se o campo referente ao professor foi renderizado
        expect(screen.getByText(/Professor:/i)).toBeVisible();

        // Verifica se o campo referente a disciplina foi renderizado
        expect(screen.getByText(/Disciplina:/i)).toBeVisible();

        // Verifica se o campo referente ao horário de início foi renderizado
        expect(screen.getByText(/Horário de Início:/i)).toBeVisible();

        // Verifica se o campo referente ao horário do fim foi renderizado
        expect(screen.getByText(/Horário do Fim:/i)).toBeVisible();

        // Verifica se o campo referente aos dias da semana foi renderizado
        expect(screen.getByText(/Dias da Semana:/i)).toBeVisible();

        // Verifica se o botão 'Alterar' foi renderizado
        expect(screen.getByRole("button", { name: /Alterar/i })).toBeVisible();

        // Verifica se o botão 'Remover' foi renderizado
        expect(screen.getByRole("button", { name: /Remover/i })).toBeVisible();

    });
    

    it("renderiza todos os dados recebidos da API", async () => {

      await waitFor(() => {

        expect(screen.getByTestId("chave_primaria")).toBeVisible();

        expect(screen.getByText("João Paulo Silva")).toBeVisible();

        expect(screen.getByText("MAT001")).toBeVisible();

        expect(screen.getByText("07:00")).toBeVisible();

        expect(screen.getByText("09:00")).toBeVisible();

        expect(screen.getByText("Segunda e Quarta")).toBeVisible();
        
        //expect(screen.getByText(/Segunda e Quarta/)).toBeVisible();

      });

    });


    it("abre modal de remover elemento", async () => {
      
      const botaoRemover = screen.getByRole("button", { name: /Remover/i });
      
      await act ( async () => {
        await userEvent.click(botaoRemover);
      });
      
      const modalRemover = screen.getByText(/Remover Aula/i);
      expect(modalRemover).toBeVisible();

    });

});