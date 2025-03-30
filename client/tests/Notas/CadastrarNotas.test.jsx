import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import CadastrarNotas from "../../src/pages/Notas/CadastrarNotas";
import Buscar from "../../src/pages/Notas/components/Buscar";
import FormularioCadastro from "../../src/pages/Notas/components/FormularioCadastro";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/nota",
  }),
  useNavigate: jest.fn(),
}));

/**
 * Testes unitários para o componente CadastrarNotas.
 * Este conjunto de testes verifica a renderização correta do componente
 * e a exibição de mensagens de sucesso/erro.
 */
describe("CadastrarNotas Component", () => {
  describe("Cadastrar Notas", () => {
    it("renderiza o formulário corretamente", () => {
      render(
        <BrowserRouter>
          <CadastrarNotas />
        </BrowserRouter>
      );
      // Verifica se o título da página foi renderizado
      expect(screen.getByText(/Cadastrar Notas/i)).toBeVisible();

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

    describe("Componente Buscar do CadastrarNota", () => {
      it("permite ao usuário digitar nos campos do formulário de busca", async () => {
        const mockRealizarBusca = jest.fn();

        render(
          <BrowserRouter>
            <Buscar
              data={{
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
              }}
              realizarBusca={mockRealizarBusca}
            />
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

        expect(
          screen.getByText("1° ano A - Ensino Fundamental")
        ).toBeInTheDocument();
        expect(screen.getByText("Matemática (MAT101)")).toBeInTheDocument();
      });

      it("verificar se o formulário está sendo enviado", async () => {
        const mockRealizarBusca = jest.fn();

        render(
          <BrowserRouter>
            <Buscar
              data={{
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
              }}
              realizarBusca={mockRealizarBusca}
            />
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

    describe("Componente Formulário do CadastrarNotas", () => {
      const mockEnviarFormulario = jest.fn();
      beforeEach(() => {
        render(
          <BrowserRouter>
            <FormularioCadastro
              alunos={[{ matricula: "202500000001", nome: "Ricardo" }]}
              enviarFormulario={mockEnviarFormulario}
            />
          </BrowserRouter>
        );
      });

      it("permite ao usuário digitar nos campos do formulário das notas", async () => {
        const notaInput = screen.getByLabelText(/Ricardo/i);
        const botao = screen.getByText(/SALVAR/i);

        await userEvent.type(notaInput, "10");
        await userEvent.click(botao);

        await waitFor(() => {
          expect(mockEnviarFormulario).toHaveBeenCalledTimes(1);
          expect(mockEnviarFormulario).toHaveBeenCalledWith({
            alunos: [{ matricula: "202500000001", nota: 10 }],
          });
        });
      });
    });
  });
});
