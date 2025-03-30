import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import AlterarAusencias from "../../src/pages/Ausencias/AlterarAusencias";
import BuscarAluno from "../../src/pages/Ausencias/components/BuscarAluno";
import FormularioAluno from "../../src/pages/Ausencias/components/FormularioAluno";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/ausencias/alterar",
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
describe("AlterarAusencias Component", () => {
  describe("Alterar Ausencias", () => {
    it("renderiza o formulário corretamente", () => {
      render(
        <BrowserRouter>
          <AlterarAusencias />
        </BrowserRouter>
      );
      // Verifica se o título da página foi renderizado
      expect(screen.getByText(/Alterar Ausências/i)).toBeVisible();

      // Verifica se o campo "Turma:" foi renderizado
      expect(screen.getByLabelText(/Turma:/i)).toBeVisible();

      // Verifica se o campo "Disciplina:" foi renderizado
      expect(screen.getByLabelText(/Disciplina:/i)).toBeVisible();

      // Verifica se o campo "Matrícula:" foi renderizado
      expect(screen.getByLabelText(/Matrícula:/i)).toBeVisible();

      // Verifica se o texto solicitando a turma e disciplina foi renderizado
      expect(
        screen.getByText(/Selecione uma turma, uma disciplina e uma matrícula./i)
      ).toBeVisible();

      // Verifica se o botão foi renderizado
      expect(screen.getByText(/BUSCAR/i)).toBeVisible();
    });

    describe("Componente Buscar do AlterarAusencias", () => {
      it("permite ao usuário digitar nos campos do formulário de busca", async () => {
        const mockRealizarBusca = jest.fn();

        render(
          <BrowserRouter>
            <BuscarAluno realizarBusca={mockRealizarBusca} />
          </BrowserRouter>
        );

        const turmaInput = screen.getByLabelText(/Turma:/i);
        const disciplinaInput = screen.getByLabelText(/Disciplina:/i);
        const matriculaInput = screen.getByLabelText(/Matrícula:/i);

        // realiza as ações
        await userEvent.selectOptions(turmaInput, "1");
        await userEvent.selectOptions(disciplinaInput, "1");
        await userEvent.type(matriculaInput, "202600000001");

        // verifica se os dados foram digitados corretamente
        await waitFor(() => {
          expect(turmaInput).toHaveValue("1");
          expect(disciplinaInput).toHaveValue("1");
          expect(matriculaInput).toHaveValue("202600000001");
        });

        expect(screen.getByText("1° ano A - Ensino Fundamental")).toBeInTheDocument();
        expect(screen.getByText("Matemática (MAT101)")).toBeInTheDocument();
      });

      it("verificar se o formulário está sendo enviado", async () => {
        const mockRealizarBusca = jest.fn();

        render(
          <BrowserRouter>
            <BuscarAluno realizarBusca={mockRealizarBusca} />
          </BrowserRouter>
        );

        const turmaInput = screen.getByLabelText(/Turma:/i);
        const disciplinaInput = screen.getByLabelText(/Disciplina:/i);
        const matriculaInput = screen.getByLabelText(/Matrícula:/i);
        const botao = screen.getByText(/BUSCAR/i);

        // realiza as ações
        await userEvent.selectOptions(turmaInput, "1");
        await userEvent.selectOptions(disciplinaInput, "1");
        await userEvent.type(matriculaInput, "202600000001");
        await userEvent.click(botao);

        await waitFor(() => {
          expect(mockRealizarBusca).toHaveBeenCalledTimes(1);
          expect(mockRealizarBusca).toHaveBeenCalledWith({
            aluno_matricula: "202600000001",
            turma: "1",
            aula_id: "1",
          });
        });
      });
    });

    describe("Componente Formulário do AlterarAusencias", () => {
      const mockEnviarFormulario = jest.fn();
      const aluno = { matricula: "202600000001", nome: "Ricardo", ausencias: 1};

      beforeEach(() => {
        render(
          <BrowserRouter>
            <FormularioAluno
              aluno={aluno}
              enviarFormulario={mockEnviarFormulario}
            />
          </BrowserRouter>
        );
      });
      

      it("permite ao usuário digitar nos campos do formulário das ausências", async () => {
        // Verifica se o campo referente ao nome foi renderizado
        expect(screen.getByText(/Nome:/i)).toBeVisible();
        expect(screen.getByText("Ricardo")).toBeVisible();

        const ausenciasInput = screen.getByLabelText(/Ausências/i);
        const botao = screen.getByText(/SALVAR/i);

        await userEvent.clear(ausenciasInput);
        await userEvent.type(ausenciasInput, "2");
        await userEvent.click(botao);

        await waitFor(() => {
          expect(mockEnviarFormulario).toHaveBeenCalledTimes(1);
          expect(mockEnviarFormulario).toHaveBeenCalledWith({
            ausencias: 2
          });
        });
      });
    });
  });
});
