import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { AlterarNotas } from "../../src/pages/Notas";
import FormularioAlterar from "../../src/pages/Notas/components/FormularioAlterar";
import BuscarAlterar from "../../src/pages/Notas/components/BuscarAlterar";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/nota",
  }),
  useNavigate: jest.fn(),
}));

describe("AlterarNotas Component", () => {
  describe("Alterar Notas", () => {
    it("renderiza o formulário corretamente", () => {});
    render(
      <BrowserRouter>
        <AlterarNotas />
      </BrowserRouter>
    );

    // Verifica se o título da página foi renderizado
    expect(screen.getByText(/Alterar Notas/i)).toBeVisible();

    // Verifica se o campo "Turma:" foi renderizado
    expect(screen.getByLabelText(/Turma:/i)).toBeVisible();

    // Verifica se o campo "Disciplina:" foi renderizado
    expect(screen.getByLabelText(/Disciplina:/i)).toBeVisible();

    // Verifica se o campo "Matrícula:" foi renderizado
    expect(screen.getByLabelText(/Matrícula:/i)).toBeVisible();

    // Verifica se o texto solicitando o aluno foi renderizado
    expect(screen.getByText(/Selecione um aluno/i)).toBeVisible();

    // Verifica se o botão foi renderizado
    expect(screen.getByText(/BUSCAR/i)).toBeVisible();
  });

  describe("BuscarComponent", () => {
    it("permite ao usuário digitar nos campos do formulário de busca", async () => {
      const mockRealizarBusca = jest.fn();

      render(
        <BrowserRouter>
          <BuscarAlterar
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
      const matriculaInput = screen.getByLabelText(/Matrícula:/i);

      // realiza as ações
      await userEvent.selectOptions(turmaInput, "1");
      await userEvent.selectOptions(disciplinaInput, "1");
      await userEvent.type(matriculaInput, "202500000001");

      // verifica se os dados foram digitados corretamente
      await waitFor(() => {
        expect(turmaInput).toHaveValue("1");
        expect(disciplinaInput).toHaveValue("1");
        expect(matriculaInput.value).toBe("202500000001");
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
          <BuscarAlterar
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
      const matriculaInput = screen.getByLabelText(/Matrícula:/i);
      const botao = screen.getByText(/BUSCAR/i);

      // realiza as ações
      await userEvent.selectOptions(turmaInput, "1");
      await userEvent.selectOptions(disciplinaInput, "1");
      await userEvent.type(matriculaInput, "202500000001");
      await userEvent.click(botao);
    });

    describe("Componente Formulário do AlterarNota", () => {
      const mockEnviarFormulario = jest.fn();
      beforeEach(() => {
        render(
          <BrowserRouter>
            <FormularioAlterar
              data={{
                aula_id: 1,
                matricula: "202500000004",
                nome: "Gabriel",
                notas: [8.0, 5.0, 4.5, 8.7],
                situacao: "M",
              }}
              enviarFormulario={mockEnviarFormulario}
            />
          </BrowserRouter>
        );
      });
      it("permite ao usuário digitar nos campos do formulário das notas", async () => {
        const u1Input = screen.getByLabelText(/1° Unidade/i);
        const u2Input = screen.getByLabelText(/2° Unidade/i);
        const u3Input = screen.getByLabelText(/3° Unidade/i);
        const u4Input = screen.getByLabelText(/4° Unidade/i);
        const botao = screen.getByText(/SALVAR/i);

        await userEvent.clear(u1Input)
        await userEvent.clear(u2Input)
        await userEvent.clear(u3Input)
        await userEvent.clear(u4Input)

        await userEvent.type(u1Input, "10");
        await userEvent.type(u2Input, "5.5");
        await userEvent.type(u3Input, "5");
        await userEvent.type(u4Input, "9.0");
        await userEvent.click(botao);

        await waitFor(() => {
          expect(mockEnviarFormulario).toHaveBeenCalledTimes(1);
          expect(mockEnviarFormulario).toHaveBeenCalledWith({
            notas: [10, 5.5, 5, 9],
          });
        });
      });
    });
  });
});
