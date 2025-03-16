import React from "react";
import {
  render,
  screen,
  fireEvent,
  waitFor,
  act
} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { FormularioTurma } from "../../src/pages/Turma";
import Formulario from "../../src/pages/Turma/components/Formulario";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/turma",
  }),
  useNavigate: jest.fn(),
}));

/**
 * Testes unitários para o componente FormularioTurma.
 * Este conjunto de testes verifica a renderização correta do componente
 * e a exibição de mensagens de sucesso/erro.
 */
describe("FormularioTurma Component", () => {
  describe("Cadastrar Turma", () => {
    beforeEach(() => {
      render(
        <BrowserRouter>
          <FormularioTurma />
        </BrowserRouter>
      );
    });

    it("renderiza o formulário corretamente", () => {
      // Verifica se o título da página foi renderizado
      expect(screen.getByText(/Cadastrar Turma/i)).toBeVisible();

      // Verifica se o campo "Ano:" foi renderizado
      expect(screen.getByLabelText(/Ano:/i)).toBeVisible();

      // Verifica se o campo "Série:" foi renderizado
      expect(screen.getByLabelText(/Série:/i)).toBeVisible();

      // Verifica se o campo "Nível de Ensino:" foi renderizado
      expect(screen.getByLabelText(/Nível de Ensino:/i)).toBeVisible();

      // Verifica se o campo "Turno:" foi renderizado
      expect(screen.getByLabelText(/Turno:/i)).toBeVisible();

      // Verifica se o campo "Número da Sala:" foi renderizado
      expect(screen.getByLabelText(/Número da Sala:/i)).toBeVisible();

      // Verifica se o campo "Ano Letivo:" foi renderizado
      expect(screen.getByLabelText(/Ano Letivo:/i)).toBeVisible();

      // Verifica se o botão foi renderizado
      expect(screen.getByText(/Finalizar/i)).toBeVisible();
    });

    it("exibe mensagem de erro ao enviar formulário sem preencher campos obrigatórios", async () => {
      // Clica no botão de finalizar sem preencher os campos obrigatórios
      const botao = screen.getByText(/Finalizar/i);
      fireEvent.click(botao);

      // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
      expect(
        await screen.findByText(/O ano da turma é obrigatório/i)
      ).toBeVisible();
      expect(await screen.findByText(/A série é obrigatória/i)).toBeVisible();
      expect(
        await screen.findByText(/O nível de ensino é obrigatório/i)
      ).toBeVisible();
      expect(await screen.findByText(/O turno é obrigatório/i)).toBeVisible();
      expect(
        await screen.findByText(/O número da sala é obrigatório/i)
      ).toBeVisible();
      expect(
        await screen.findByText(/O ano letivo é obrigatório/i)
      ).toBeVisible();
    });

    it("permite ao usuário digitar nos campos do formulário", async () => {
      const anoInput = screen.getByLabelText(/Ano:/i);
      const serieInput = screen.getByLabelText(/Série:/i);
      const nivelEnsinoInput = screen.getByLabelText(/Nível de Ensino:/i);
      const turnoInput = screen.getByLabelText(/Turno:/i);
      const numeroSalaInput = screen.getByLabelText(/Número da Sala:/i);
      const anoLetivoInput = screen.getByLabelText(/Ano Letivo:/i);

      // realiza as ações
      await act(async () => {
        await userEvent.type(anoInput, "1");
        await userEvent.type(serieInput, "A");
        await userEvent.selectOptions(nivelEnsinoInput, "Ensino Fundamental");
        await userEvent.selectOptions(turnoInput, "M");
        await userEvent.type(numeroSalaInput, "123");
        await userEvent.type(anoLetivoInput, "2026");
      });

      // verifica se os dados foram digitados corretamente
      expect(anoInput.value).toBe("1");
      expect(serieInput.value).toBe("A");
      expect(nivelEnsinoInput.value).toBe("Ensino Fundamental");
      expect(turnoInput.value).toBe("M");
      expect(numeroSalaInput.value).toBe("123");
      expect(anoLetivoInput.value).toBe("2026");
    });
  });

  describe("Formulario da Turma", () => {
    const mockEnviarFormulario = jest.fn();

    beforeEach(() => {
      render(
        <BrowserRouter>
          <Formulario
            enviarFormulario={mockEnviarFormulario}
            alteracao={{
              alterar: false,
              dados: {},
              chave: undefined,
            }}
          />
        </BrowserRouter>
      );
    });

    it("verificar se o formulário está sendo enviado", async () => {

      const anoInput = screen.getByLabelText(/Ano:/i);
      const serieInput = screen.getByLabelText(/Série:/i);
      const nivelEnsinoInput = screen.getByLabelText(/Nível de Ensino:/i);
      const turnoInput = screen.getByLabelText(/Turno:/i);
      const numeroSalaInput = screen.getByLabelText(/Número da Sala:/i);
      const anoLetivoInput = screen.getByLabelText(/Ano Letivo:/i);
      const botao = screen.getByText(/Finalizar/i);

      // realiza as ações
      await act(async () => {
        await userEvent.type(anoInput, "1");
        await userEvent.type(serieInput, "A");
        await userEvent.selectOptions(nivelEnsinoInput, "Ensino Fundamental");
        await userEvent.selectOptions(turnoInput, "M");
        await userEvent.type(numeroSalaInput, "123");
        await userEvent.type(anoLetivoInput, "2026");
        await userEvent.click(botao);
      });

      await waitFor(() => {
        expect(mockEnviarFormulario).toHaveBeenCalledTimes(1);
        expect(mockEnviarFormulario).toHaveBeenCalledWith(
          {
            ano: 1,
            serie: "A",
            nivel_de_ensino: "Ensino Fundamental",
            turno: "M",
            sala_numero: 123,
            calendario_ano_letivo: 2026,
          }
        );
      });
    });
  });
});
