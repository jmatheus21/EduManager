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
import { FormularioAluno } from "../../src/pages/Aluno";
import Formulario from "../../src/pages/Aluno/components/Formulario";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/aluno",
  }),
  useNavigate: jest.fn(),
}));

/**
 * Testes unitários para o componente FormularioAluno.
 * Este conjunto de testes verifica a renderização correta do componente
 * e a exibição de mensagens de sucesso/erro.
 */
describe("FormularioAluno Component", () => {
  describe("Cadastrar Aluno", () => {
    beforeEach(() => {
      render(
        <BrowserRouter>
          <FormularioAluno />
        </BrowserRouter>
      );
    });

    it("renderiza o formulário corretamente", () => {
      // Verifica se o título da página foi renderizado
      expect(screen.getByText(/Cadastrar Aluno/i)).toBeVisible();

      // Verifica se o campo "Aluno:" foi renderizado
      expect(screen.getByLabelText(/Aluno:/i)).toBeVisible();

      // Verifica se o campo "Email:" foi renderizado
      expect(screen.getByLabelText(/Email:/i)).toBeVisible();

      // Verifica se o campo "Telefone:" foi renderizado
      expect(screen.getByLabelText(/Telefone:/i)).toBeVisible();

      // Verifica se o campo "Data de Nascimento:" foi renderizado
      expect(screen.getByLabelText(/Data de Nascimento:/i)).toBeVisible();

      // Verifica se o campo "Endereço:" foi renderizado
      expect(screen.getByLabelText(/Endereço:/i)).toBeVisible();

      // Verifica se o campo "Id da Turma:" foi renderizado
      expect(screen.getByLabelText(/Id da Turma:/i)).toBeVisible();

      // Verifica se o botão foi renderizado
      expect(screen.getByText(/Finalizar/i)).toBeVisible();
    });

    it("exibe mensagem de erro ao enviar formulário sem preencher campos obrigatórios", async () => {
      // Clica no botão de finalizar sem preencher os campos obrigatórios
      const botao = screen.getByText(/Finalizar/i);
      fireEvent.click(botao);

      // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
      expect(
        await screen.findByText(/O nome é obrigatório/i)
      ).toBeVisible();
      expect(await screen.findByText(/O e-mail é obrigatório/i)).toBeVisible();
      expect(
        await screen.findByText(/O telefone é obrigatório/i)
      ).toBeVisible();
      expect(await screen.findByText(/A data de nascimento é obrigatória/i)).toBeVisible();
      expect(
        await screen.findByText(/O endereço é obrigatório/i)
      ).toBeVisible();
      expect(
        await screen.findByText(/O id da turma é obrigatório/i)
      ).toBeVisible();
    });

    it("permite ao usuário digitar nos campos do formulário", async () => {
      const nomeInput = screen.getByLabelText(/Aluno:/i);
      const emailInput = screen.getByLabelText(/Email:/i);
      const telefoneInput = screen.getByLabelText(/Telefone:/i);
      const dataDeNascimentoInput = screen.getByLabelText(/Data de Nascimento:/i);
      const enderecoInput = screen.getByLabelText(/Endereço:/i);
      const idDaTurmaInput = screen.getByLabelText(/Id da Turma:/i);

      // realiza as ações
      await act(async () => {
        await userEvent.type(nomeInput, "João Pedro dos Santos");
        await userEvent.type(emailInput, "joaopedro@email.com");
        await userEvent.type(telefoneInput, "79 9 1234-5678");
        await userEvent.type(dataDeNascimentoInput, "2011-09-10");
        await userEvent.type(enderecoInput, "Bairro X, Rua A");
        await userEvent.type(idDaTurmaInput, "1");
      });

      // verifica se os dados foram digitados corretamente
      expect(nomeInput.value).toBe("João Pedro dos Santos");
      expect(emailInput.value).toBe("joaopedro@email.com");
      expect(telefoneInput.value).toBe("79 9 1234-5678");
      expect(dataDeNascimentoInput.value).toBe("2011-09-10");
      expect(enderecoInput.value).toBe("Bairro X, Rua A");
      expect(idDaTurmaInput.value).toBe("1");
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

    it. ("verificar se o formulário está sendo enviado", async () => {

      const nomeInput = screen.getByLabelText(/Aluno:/i);
      const emailInput = screen.getByLabelText(/Email:/i);
      const telefoneInput = screen.getByLabelText(/Telefone:/i);
      const dataDeNascimentoInput = screen.getByLabelText(/Data de Nascimento:/i);
      const enderecoInput = screen.getByLabelText(/Endereço:/i);
      const idDaTurmaInput = screen.getByLabelText(/Id da Turma:/i);
      const botao = screen.getByText(/Finalizar/i);

      // realiza as ações
      await act(async () => {
        await userEvent.type(nomeInput, "João Pedro dos Santos");
        await userEvent.type(emailInput, "joaopedro@email.com");
        await userEvent.type(telefoneInput, "79 9 1234-5678");
        await userEvent.type(dataDeNascimentoInput, "2011-09-10");
        await userEvent.type(enderecoInput, "Bairro X, Rua A");
        await userEvent.type(idDaTurmaInput, "1");
        await userEvent.click(botao);
      });

      await waitFor(() => {
        expect(mockEnviarFormulario).toHaveBeenCalledTimes(1);
        expect(mockEnviarFormulario).toHaveBeenCalledWith(
          {
            nome: "João Pedro dos Santos",
            email: "joaopedro@email.com",
            telefone: "79 9 1234-5678",
            data_de_nascimento: "2011-09-10",
            endereco: "Bairro X, Rua A",
            turma_id: 1
          });
      });
    });
  });

  describe("Teste de alterar aluno", () => {

    const mockEnviarFormulario = jest.fn();

    beforeEach(() => {
      render(
        <BrowserRouter>
          <Formulario enviarFormulario={mockEnviarFormulario}
          alteracao={{
            alterar: true,
            dados: {
              matricula: "202600000001",
              nome: "João Pedro dos Santos",
              email: "joaopedro@email.com",
              telefone: "79 9 1234-5678",
              data_de_nascimento: "2011-09-10",
              endereco: "Bairro X, Rua A",
              turma_id: 1
            },
            chave: "202600000001"
            }}
          />
        </BrowserRouter>
      )
    });
    
    it ("verifica se os dados foram carregados", async () => {

      // pegar os campos
      const nomeInput = screen.getByLabelText(/Aluno:/i);
      const emailInput = screen.getByLabelText(/Email:/i);
      const telefoneInput = screen.getByLabelText(/Telefone:/i);
      const dataDeNascimentoInput = screen.getByLabelText(/Data de Nascimento:/i);
      const enderecoInput = screen.getByLabelText(/Endereço:/i);
      const idDaTurmaInput = screen.getByLabelText(/Id da Turma:/i);


      await waitFor(() => {
        // verificar se estão com os valores que recebe
        expect(nomeInput.value).toBe("João Pedro dos Santos");
        expect(emailInput.value).toBe("joaopedro@email.com");
        expect(telefoneInput.value).toBe("79 9 1234-5678");
        expect(dataDeNascimentoInput.value).toBe("2011-09-10");
        expect(enderecoInput.value).toBe("Bairro X, Rua A");
        expect(idDaTurmaInput.value).toBe("1");
      })

    });

  });
});
