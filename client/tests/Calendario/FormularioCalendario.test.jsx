import React from "react";
import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { FormularioCalendario } from "../../src/pages/Calendario"
import Formulario from "../../src/pages/Calendario/components/Formulario";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/calendario"
  }),
  useNavigate: jest.fn(),
}));

/**
 * Testes unitários para o componente FormularioCalendario.
 * Este conjunto de testes verifica a renderização correta do componente
 * e a exibição de mensagens de sucesso/erro.
 */
describe("FormularioCalendario Component", () => {

  describe("Cadastrar Calendario", () => {

    beforeEach(() => {
      render(
          <BrowserRouter>
              <FormularioCalendario/>
          </BrowserRouter>
      );
    })

    it ("renderiza o formulário corretamente", () => {

      // Verifica se o título da página foi renderizado
      expect(screen.getByText(/Cadastrar Calendário/i)).toBeVisible();
  
      // Verifica se o campo "Ano letivo" foi renderizado
      expect(screen.getByLabelText(/Ano letivo:/i)).toBeVisible();
  
      // Verifica se o campo "Dias letivos" foi renderizado
      expect(screen.getByLabelText(/Dias letivos:/i)).toBeVisible();
  
      // Verifica se o campo "Data de início" foi renderizado
      expect(screen.getByLabelText(/Data de início:/i)).toBeVisible();

      // Verifica se o campo "Data de fim" foi renderizado
      expect(screen.getByLabelText(/Data de fim:/i)).toBeVisible();
  
      // Verifica se o botão foi renderizado
      expect(screen.getByText(/Finalizar/i)).toBeVisible();

    });

    it ("exibe mensagem de erro ao enviar formulário sem preencher campos obrigatórios", async () => {
  
      // Clica no botão de finalizar sem preencher os campos obrigatórios
      const botao = screen.getByText(/Finalizar/i);
      fireEvent.click(botao);
  
      // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
      expect(await screen.findByText(/O ano letivo é obrigatório/i)).toBeVisible();
      expect(await screen.findByText(/A quantidade de dias letivos é obrigatória/i)).toBeVisible();
      expect(await screen.findByText(/A data de início é obrigatória/i)).toBeVisible();
      expect(await screen.findByText(/A data de fim é obrigatória/i)).toBeVisible();

    });

    it ("permite ao usuário digitar nos campos do formulário", async () => {
  
      const anoLetivoInput = screen.getByLabelText(/Ano letivo:/i);
      const diasLetivosInput = screen.getByLabelText(/Dias letivos:/i);
      const dataDeInicioInput = screen.getByLabelText(/Data de início:/i);
      const dataDeFimInput = screen.getByLabelText(/Data de fim:/i);

      // realiza as ações
      await act(async () => {
        await userEvent.type(anoLetivoInput, "2026");
        await userEvent.type(diasLetivosInput, "150");
        await userEvent.type(dataDeInicioInput, "2026-01-01");
        await userEvent.type(dataDeFimInput, "2026-09-01");
      })
      
      // verifica se os dados foram digitados corretamente
      expect(anoLetivoInput.value).toBe("2026");
      expect(diasLetivosInput.value).toBe("150");
      expect(dataDeInicioInput.value).toBe("2026-01-01");
      expect(dataDeFimInput.value).toBe("2026-09-01");

    });

  });

  describe("Formulario do Calendario", () => {

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

    it ("verificar se o formulário está sendo enviado", async () => {

      const anoLetivoInput = screen.getByLabelText(/Ano letivo:/i);
      const diasLetivosInput = screen.getByLabelText(/Dias letivos:/i);
      const dataDeInicioInput = screen.getByLabelText(/Data de início:/i);
      const dataDeFimInput = screen.getByLabelText(/Data de fim:/i);
      const botao = screen.getByText(/Finalizar/i);

      // realiza as ações
      await act(async () => {
        await userEvent.type(anoLetivoInput, "2026");
        await userEvent.type(diasLetivosInput, "150");
        await userEvent.type(dataDeInicioInput, "2026-01-01");
        await userEvent.type(dataDeFimInput, "2026-09-01");
        await userEvent.click(botao);
      });

      await waitFor(() => {
        expect(mockEnviarFormulario).toHaveBeenCalledTimes(1);
        expect(mockEnviarFormulario).toHaveBeenCalledWith({
          ano_letivo: 2026,
          dias_letivos: 150,
          data_inicio: "2026-01-01",
          data_fim: "2026-09-01"
        }, expect.anything());
      });

    })

  })

  describe("Alterar Calendario", () => {

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
                      ano_letivo: 2026,
                      dias_letivos: 170,
                      data_inicio: "2026-02-01",
                      data_fim: "2026-08-01"
                    }, 
                    chave: undefined
                  }}
                />
            </BrowserRouter>
        );
      })
    })

    it ("Verifica se os dados são carregados na página de alterar", async () => {

      const anoLetivoInput = screen.getByLabelText(/Ano letivo:/i);
      const diasLetivosInput = screen.getByLabelText(/Dias letivos:/i);
      const dataDeInicioInput = screen.getByLabelText(/Data de início:/i);
      const dataDeFimInput = screen.getByLabelText(/Data de fim:/i);
      
      await waitFor(() => {
        expect(anoLetivoInput.value).toBe("2026");
        expect(diasLetivosInput.value).toBe("170");
        expect(dataDeInicioInput.value).toBe("2026-02-01")
        expect(dataDeFimInput.value).toBe("2026-08-01")
      })
    });

  });
});