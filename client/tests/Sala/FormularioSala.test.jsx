import React from "react";
import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { FormularioSala } from "../../src/pages/Sala"
import Formulario from "../../src/pages/Sala/components/Formulario";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/sala"
  }),
  useNavigate: jest.fn(),
}));

/**
 * Testes unitários para o componente FormularioSala.
 * Este conjunto de testes verifica a renderização correta do componente
 * e a exibição de mensagens de sucesso/erro.
 */
describe("FormularioSala Component", () => {

  describe("Cadastrar Sala", () => {

    beforeEach(() => {
      render(
          <BrowserRouter>
              <FormularioSala/>
          </BrowserRouter>
      );
    })

    it("renderiza o formulário corretamente", () => {

      // Verifica se o título da página foi renderizado
      expect(screen.getByText(/Cadastrar Sala/i)).toBeVisible();
  
      // Verifica se o campo "Número:" foi renderizado
      expect(screen.getByLabelText(/Número:/i)).toBeVisible();
  
      // Verifica se o campo "Capacidade:" foi renderizado
      expect(screen.getByLabelText(/Capacidade:/i)).toBeVisible();
  
      // Verifica se o campo "Localização:" foi renderizado
      expect(screen.getByLabelText(/Localização:/i)).toBeVisible();
  
      // Verifica se o botão foi renderizado
      expect(screen.getByText(/Finalizar/i)).toBeVisible();

    });

    it("exibe mensagem de erro ao enviar formulário sem preencher campos obrigatórios", async () => {
  
      // Clica no botão de finalizar sem preencher os campos obrigatórios
      const botao = screen.getByText(/Finalizar/i);
      fireEvent.click(botao);
  
      // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
      expect(await screen.findByText(/O número é obrigatório/i)).toBeVisible();
      expect(await screen.findByText(/A capacidade é obrigatória/i)).toBeVisible();
      expect(await screen.findByText(/A localização é obrigatória/i)).toBeVisible();

    });

    it("permite ao usuário digitar nos campos do formulário", async () => {
  
      const numeroInput = screen.getByLabelText(/Número:/i);
      const capacidadeInput = screen.getByLabelText(/Capacidade:/i);
      const localizacaoInput = screen.getByLabelText(/Localização:/i);

      // realiza as ações
      await act(async () => {
        await userEvent.type(numeroInput, "123");
        await userEvent.type(capacidadeInput, "250");
        await userEvent.type(localizacaoInput, "Bloco A, 1° Andar");
      })
      
      // verifica se os dados foram digitados corretamente
      expect(numeroInput.value).toBe("123");
      expect(capacidadeInput.value).toBe("250");
      expect(localizacaoInput.value).toBe("Bloco A, 1° Andar");

    });

  });

  describe("Formulario da Sala", () => {

    const mockEnviarFormulario = jest.fn();

    beforeEach(() => {
      render(
          <BrowserRouter>
              <Formulario 
                enviarFormulario={mockEnviarFormulario} 
                alteracao={{
                  alterar: false, 
                  dados: {}, 
                  chave: undefined
                }}
              />
          </BrowserRouter>
      );
    })

    it("verificar se o formulário está sendo enviado", async () => {

      const numeroInput = screen.getByLabelText(/Número:/i);
      const capacidadeInput = screen.getByLabelText(/Capacidade:/i);
      const localizacaoInput = screen.getByLabelText(/Localização:/i);
      const botao = screen.getByText(/Finalizar/i);

      // realiza as ações
      await act(async () => {
        await userEvent.type(numeroInput, "123");
        await userEvent.type(capacidadeInput, "250");
        await userEvent.type(localizacaoInput, "Bloco A, 1° Andar");
        await userEvent.click(botao);
      });

      await waitFor(() => {
        expect(mockEnviarFormulario).toHaveBeenCalledTimes(1);
        expect(mockEnviarFormulario).toHaveBeenCalledWith({
          numero: 123,
          capacidade: 250,
          localizacao: "Bloco A, 1° Andar"
        }, expect.anything());
      });

    })

  })

  describe("Alterar Sala", () => {

    const mockEnviarFormulario = jest.fn();

    beforeEach( async () => {
      await act(async () => {
        render(
            <BrowserRouter>
                <Formulario 
                  enviarFormulario={mockEnviarFormulario} 
                  alteracao={{
                    alterar: true, 
                    dados: {
                      numero: 123,
                      capacidade: 100,
                      localizacao: "Bloco A, 1° Andar"
                    }, 
                    chave: undefined
                  }}
                />
            </BrowserRouter>
        );
      })

    })

    it("Verifica se os dados são carregados na página de alterar", async () => {

      const numeroInput = screen.getByLabelText(/Número:/i);
      const capacidadeInput = screen.getByLabelText(/Capacidade:/i);
      const localizacaoInput = screen.getByLabelText(/Localização:/i);

      await waitFor(() => {
        expect(numeroInput.value).toBe("123");
        expect(capacidadeInput.value).toBe("100");
        expect(localizacaoInput.value).toBe("Bloco A, 1° Andar")
      })

    });

  });

});