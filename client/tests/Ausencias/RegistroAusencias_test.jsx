import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import RegistroAusencias from "../../src/pages/Ausencias/RegistroAusencias";
import Buscar from "../../src/pages/Ausencias/components/Buscar";
import Formulario from "../../src/pages/Ausencias/components/Formulario";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/ausencias",
  }),
  useNavigate: jest.fn(),
}));

jest.mock("../../src/hooks/useApi", () => ({
  __esModule: true,
  default: () => ({
    fetchData: jest.fn(),
    data: {
      turmas: [
        {
          id: 1,
          ano: 1,
          serie: "A",
          nivel_de_ensino: "Ensino Fundamental",
        },
      ],
      disciplinas: [
        {
          turma_id: 1,
          codigo: "MAT101",
          nome: "Matemática",
          aula_id: 1,
        },
      ],
    },
  }),
}));

/**
 * Testes unitários para o componente RegistroAusencias.
 * Este conjunto de testes verifica a renderização correta do componente
 * e a exibição de mensagens de sucesso/erro.
 */
describe("RegistroAusencias Component", () => {
  describe("Registrar Ausencias", () => {
    it("renderiza o formulário corretamente", () => {
      render(
        <BrowserRouter>
          <RegistroAusencias />
        </BrowserRouter>
      );
      // Verifica se o título da página foi renderizado
      expect(screen.getByText(/Registrar Ausências/i)).toBeVisible();

      // Verifica se o campo "Turma:" foi renderizado
      expect(screen.getByLabelText(/Turma:/i)).toBeVisible();

      // Verifica se o campo "Disciplina:" foi renderizado
      expect(screen.getByLabelText(/Disciplina:/i)).toBeVisible();

      // Verifica se o texto solicitando a turma e disciplina foi renderizado
      expect(
        screen.getByText(/Selecione uma turma e uma disciplina/i)
      ).toBeVisible();

      // Verifica se o botão foi renderizado
      expect(screen.getByText(/BUSCAR/i)).toBeVisible();
    });

    describe("Componente Buscar do RegistroAusencias", () => {
      it("permite ao usuário digitar nos campos do formulário de busca", async () => {
        const mockRealizarBusca = jest.fn();

        render(
          <BrowserRouter>
            <Buscar realizarBusca={mockRealizarBusca} />
          </BrowserRouter>
        );

        const turmaInput = screen.getByLabelText(/Turma:/i);
        const disciplinaInput = screen.getByLabelText(/Disciplina:/i);

        // realiza as ações
        await userEvent.selectOptions(turmaInput, "1");
        await userEvent.selectOptions(disciplinaInput, "1");

        // verifica se os dados foram digitados corretamente
        await waitFor(() => {
          expect(turmaInput).toHaveValue("1");
          expect(disciplinaInput).toHaveValue("1");
        });

        expect(screen.getByText("1° ano A - Ensino Fundamental")).toBeInTheDocument();
        expect(screen.getByText("Matemática (MAT101)")).toBeInTheDocument();
      });

      it("verificar se o formulário está sendo enviado", async () => {
        const mockRealizarBusca = jest.fn();

        render(
          <BrowserRouter>
            <Buscar realizarBusca={mockRealizarBusca} />
          </BrowserRouter>
        );

        const turmaInput = screen.getByLabelText(/Turma:/i);
        const disciplinaInput = screen.getByLabelText(/Disciplina:/i);
        const botao = screen.getByText(/BUSCAR/i);

        // realiza as ações
        await userEvent.selectOptions(turmaInput, "1");
        await userEvent.selectOptions(disciplinaInput, "1");
        await userEvent.click(botao);

        await waitFor(() => {
          expect(mockRealizarBusca).toHaveBeenCalledTimes(1);
          expect(mockRealizarBusca).toHaveBeenCalledWith({
            turma: "1",
            aula_id: "1",
          });
        });
      });
    });

    describe("Componente Formulário do RegistroAusencias", () => {
      const mockEnviarFormulario = jest.fn();
      const alunos = [{ matricula: "202600000001", nome: "Ricardo" },
                      { matricula: "202600000002", nome: "Maria" }
                     ];

      beforeEach(() => {
        render(
          <BrowserRouter>
            <Formulario
              alunos={alunos}
              enviarFormulario={mockEnviarFormulario}
            />
          </BrowserRouter>
        );
      });
      

      it("permite ao usuário digitar nos campos do formulário das ausências", async () => {
        const ausencia1 = screen.getByRole('checkbox', { name: /Ricardo/i });
        const ausencia2 = screen.getByRole('checkbox', { name: /Maria/i });
        const botao = screen.getByText(/SALVAR/i);

        await userEvent.click(ausencia1);
        await userEvent.click(ausencia2);
        await userEvent.click(botao);

        await waitFor(() => {
          expect(mockEnviarFormulario).toHaveBeenCalledTimes(1);
          expect(mockEnviarFormulario).toHaveBeenCalledWith({
            alunos: [{ matricula: "202600000001", ausencia: true },
                     { matricula: "202600000002", ausencia: true }                
                    ],
          });
        });
      });
    });
  });
});
