import React from "react";
import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { FormularioDisciplina } from "../../src/pages/Disciplina"
import Formulario from "../../src/pages/Disciplina/components/Formulario";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/disciplina"
  }),
  useNavigate: jest.fn(),
}));

/**
 * Testes unitários para o componente FormularioDisciplina.
 * Este conjunto de testes verifica a renderização correta do componente
 * e a exibição de mensagens de sucesso/erro.
 */
describe("FormularioDisciplina Component", () => {

  describe("Cadastrar Disciplina", () => {

    beforeEach(() => {
      render(
          <BrowserRouter>
              <FormularioDisciplina/>
          </BrowserRouter>
      );
    })

    it ("renderiza o formulário corretamente", () => {

      // Verifica se o título da página foi renderizado
      expect(screen.getByText(/Cadastrar Disciplina/i)).toBeVisible();
  
      // Verifica se o campo "Nome:" foi renderizado
      expect(screen.getByLabelText(/Nome:/i)).toBeVisible();
  
      // Verifica se o campo "Código:" foi renderizado
      expect(screen.getByLabelText(/Código:/i)).toBeVisible();
  
      // Verifica se o campo "Carga Horária:" foi renderizado
      expect(screen.getByLabelText(/Carga Horária:/i)).toBeVisible();

      // Verifica se o campo "Ementa:" foi renderizado
      expect(screen.getByLabelText(/Ementa:/i)).toBeVisible();

      // Verifica se o campo "Bibliografia:" foi renderizado
      expect(screen.getByLabelText(/Bibliografia:/i)).toBeVisible();
  
      // Verifica se o botão foi renderizado
      expect(screen.getByText(/Finalizar/i)).toBeVisible();

    });

    it ("exibe mensagem de erro ao enviar formulário sem preencher campos obrigatórios", async () => {
  
      // Clica no botão de finalizar sem preencher os campos obrigatórios
      const botao = screen.getByText(/Finalizar/i);
      fireEvent.click(botao);
  
      // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
      expect(await screen.findByText(/O nome da disciplina é obrigatório/i)).toBeVisible();
      expect(await screen.findByText(/O código da disciplina é obrigatório/i)).toBeVisible();
      expect(await screen.findByText(/A carga horária é obrigatória/i)).toBeVisible();

    });

    it ("permite ao usuário digitar nos campos do formulário", async () => {
  
      const codigoInput = screen.getByLabelText(/Código:/i);
      const nomeInput = screen.getByLabelText(/Nome:/i);
      const cargaHorariaInput = screen.getByLabelText(/Carga Horária:/i);
      const ementaInput = screen.getByLabelText(/Ementa:/i);
      const bibliografiaInput = screen.getByLabelText(/Bibliografia:/i);

      // realiza as ações
      await act(async () => {
        await userEvent.type(codigoInput, "MAT101");
        await userEvent.type(nomeInput, "Matemática");
        await userEvent.type(cargaHorariaInput, "60");
        await userEvent.type(ementaInput, "Aritmética e Álgebra");
        await userEvent.type(bibliografiaInput, "Matemática - Volume 1");
      })
      
      // verifica se os dados foram digitados corretamente
      expect(codigoInput.value).toBe("MAT101");
      expect(nomeInput.value).toBe("Matemática");
      expect(cargaHorariaInput.value).toBe("60");
      expect(ementaInput.value).toBe("Aritmética e Álgebra");
      expect(bibliografiaInput.value).toBe("Matemática - Volume 1");

    });

  });

  describe("Formulario da Disciplina", () => {

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

      const codigoInput = screen.getByLabelText(/Código:/i);
      const nomeInput = screen.getByLabelText(/Nome:/i);
      const cargaHorariaInput = screen.getByLabelText(/Carga Horária:/i);
      const ementaInput = screen.getByLabelText(/Ementa:/i);
      const bibliografiaInput = screen.getByLabelText(/Bibliografia:/i);
      const botao = screen.getByText(/Finalizar/i);

      // realiza as ações
      await act(async () => {
        await userEvent.type(codigoInput, "MAT101");
        await userEvent.type(nomeInput, "Matemática");
        await userEvent.type(cargaHorariaInput, "60");
        await userEvent.type(ementaInput, "Aritmética e Álgebra");
        await userEvent.type(bibliografiaInput, "Matemática - Volume 1");
        await userEvent.click(botao);
      });

      await waitFor(() => {
        expect(mockEnviarFormulario).toHaveBeenCalledTimes(1);
        expect(mockEnviarFormulario).toHaveBeenCalledWith({
          codigo: "MAT101",
          nome: "Matemática",
          carga_horaria: 60,
          ementa: "Aritmética e Álgebra",
          bibliografia: "Matemática - Volume 1"
        });
      });

    })

  })

  describe("Alterar Disciplina", () => {

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
                      codigo: "MAT101",
                      nome: "Matemática 1",
                      carga_horaria: 90,
                      ementa: "Aritmética e Álgebra",
                      bibliografia: "Matemática - Volume 1"
                    }, 
                    chave: undefined
                  }}
                />
            </BrowserRouter>
        );
      })

    })

    it ("Verifica se os dados são carregados na página de alterar", async () => {

      const codigoInput = screen.getByLabelText(/Código:/i);
      const nomeInput = screen.getByLabelText(/Nome:/i);
      const cargaHorariaInput = screen.getByLabelText(/Carga Horária:/i);
      const ementaInput = screen.getByLabelText(/Ementa:/i);
      const bibliografiaInput = screen.getByLabelText(/Bibliografia:/i);

      await waitFor(() => {
        expect(codigoInput.value).toBe("MAT101");
        expect(nomeInput.value).toBe("Matemática 1");
        expect(cargaHorariaInput.value).toBe("90");
        expect(ementaInput.value).toBe("Aritmética e Álgebra");
        expect(bibliografiaInput.value).toBe("Matemática - Volume 1")
      })
    });
  });
});
