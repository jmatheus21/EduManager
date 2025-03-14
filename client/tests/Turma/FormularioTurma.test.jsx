import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import  { FormularioTurma } from "../../src/pages/Turma"

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: jest.fn(),
  useNavigate: jest.fn(),
}));

/**
 * Testes unitários para o componente FormularioTurma.
 * Este conjunto de testes verifica a renderização correta do componente
 * e a exibição de mensagens de sucesso/erro.
 */
describe("ConsultarTurma Component", () => {
    it("renderiza o formulário corretamente", () => {
      render(
          <BrowserRouter>
              <FormularioTurma/>
          </BrowserRouter>
      );
  
      // Verifica se o título da página foi renderizado
      expect(screen.getByText(/Cadastrar Turma/i)).toBeInTheDocument();
  
      // Verifica se o campo "Ano:" foi renderizado
      expect(screen.getByLabelText(/Ano:/i)).toBeInTheDocument();
  
      // Verifica se o campo "Série:" foi renderizado
      expect(screen.getByLabelText(/Série:/i)).toBeInTheDocument();
  
      // Verifica se o campo "Nível de Ensino:" foi renderizado
      expect(screen.getByLabelText(/Nível de Ensino:/i)).toBeInTheDocument();
  
      // Verifica se o campo "Turno:" foi renderizado
      expect(screen.getByLabelText(/Turno:/i)).toBeInTheDocument();
  
      // Verifica se o campo "Número da Sala:" foi renderizado
      expect(screen.getByLabelText(/Número da Sala:/i)).toBeInTheDocument();

      // Verifica se o campo "Ano Letivo:" foi renderizado
      expect(screen.getByLabelText(/Ano Letivo:/i)).toBeInTheDocument();
  
      // Verifica se o botão foi renderizado
      expect(screen.getByText(/Finalizar/i)).toBeInTheDocument();
    });
  
    it("exibe mensagem de erro ao enviar formulário sem preencher campos obrigatórios", async () => {
      render(
          <BrowserRouter>
              <FormularioTurma/>
          </BrowserRouter>
      );
  
      // Clica no botão de finalizar sem preencher os campos obrigatórios
      const botao = screen.getByText(/Finalizar/i)
      fireEvent.click(botao);
  
      // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
      expect(await screen.findByText(/O ano da turma é obrigatório/i)).toBeInTheDocument();
  
      expect(await screen.findByText(/A série é obrigatória/i)).toBeInTheDocument();
  
      expect(await screen.findByText(/O nível de ensino é obrigatório/i)).toBeInTheDocument();

      expect(await screen.findByText(/O turno é obrigatório/i)).toBeInTheDocument();

      expect(await screen.findByText(/O número da sala é obrigatório/i)).toBeInTheDocument();

      expect(await screen.findByText(/O ano letivo é obrigatório/i)).toBeInTheDocument();
    });
  
    it("permite ao usuário digitar nos campos do formulário", () => {
      render(
          <BrowserRouter>
              <FormularioTurma/>
          </BrowserRouter>
      );
  
      // busca o campo de código e simula a digitação de um nome
      // exemplo com tipo number
      const anoInput = screen.getByLabelText(/Ano:/i);
      fireEvent.change(anoInput, { target: { value: 9 } });
  
      // exemplo com tipo text
      const serieInput = screen.getByLabelText(/Série:/i);
      fireEvent.change(serieInput, { target: { value: "A" } });
  
      // exemplo com tipo text
      const nivelDeEnsinoInput = screen.getByLabelText(/Nível de Ensino:/i);
      fireEvent.change(nivelDeEnsinoInput, { target: { value: "Ensino Fundamental" } });
  
      // exemplo com tipo text
      const turnoInput = screen.getByLabelText(/Turno:/i);
      fireEvent.change(turnoInput, { target: { value: "D" } });
  
      // exemplo com tipo number
      const salaNumeroInput = screen.getByLabelText(/Número da Sala:/i);
      fireEvent.change(salaNumeroInput, { target: { value: 101 } });

      // exemplo com tipo number
      const calendarioAnoLetivoInput = screen.getByLabelText(/Ano Letivo:/i);
      fireEvent.change(calendarioAnoLetivoInput, { target: { value: 2026 } });
      
      // verifica se o dado foi digitado corretamente
      expect(anoInput.value).toBe("9");
      expect(serieInput.value).toBe("A");
      expect(nivelDeEnsinoInput.value).toBe("Ensino Fundamental");
      expect(turnoInput.value).toBe("D");
      expect(salaNumeroInput.value).toBe("101"); 
      expect(calendarioAnoLetivoInput.value).toBe("2026"); 
    });
  
    it("exibe mensagem de erro ao enviar formulário com o número de caracteres menor do que o mínimo", async () => {
      render(
          <BrowserRouter>
              <FormularioTurma/>
          </BrowserRouter>
      );
  
      const anoInput = screen.getByLabelText(/Ano:/i);
      fireEvent.change(anoInput, { target: { value: "0" } });
  
      const salaNumeroInput = screen.getByLabelText(/Número da Sala:/i);
      fireEvent.change(salaNumeroInput, { target: { value: "0" } });

      // Clica no botão de finalizar com o número de caracteres menor do que o mínimo em algum campo
      const botao = screen.getByText(/Finalizar/i)
      fireEvent.click(botao);
  
      // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
      expect(await screen.findByText(/O ano da turma deve ser no mínimo 1/i)).toBeInTheDocument();
      expect(await screen.findByText(/O número da sala deve ser no mínimo 1/i)).toBeInTheDocument();

    });

  
    it("exibe mensagem de erro ao enviar formulário com o número de caracteres maior do que o máximo", async () => {
      
      render(
        <BrowserRouter>
            <FormularioTurma/>
        </BrowserRouter>
      );
  
    // exemplo com tipo number
      const anoInput = screen.getByLabelText(/Ano:/i);
      fireEvent.change(anoInput, { target: { value: "10" } });
  
      // exemplo com tipo text
      const serieInput = screen.getByLabelText(/Série:/i);
      fireEvent.change(serieInput, { target: { value: "AA" } });

      // exemplo com tipo select
      const salaNumeroInput = screen.getByLabelText(/Número da Sala:/i);
      fireEvent.change(salaNumeroInput, { target: { value: "1001" } });

      // Clica no botão de finalizar com número de caracteres maior do que o máximo permitido
      const botao = screen.getByText(/Finalizar/i)
      fireEvent.click(botao);
  
      // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
      expect(await screen.findByText(/O ano da turma deve ser no máximo 9/i)).toBeInTheDocument();
      expect(await screen.findByText(/A série deve ter no máximo 1 caractere/i)).toBeInTheDocument();
      expect(await screen.findByText(/O número da sala deve ser de no máximo 1000/i)).toBeInTheDocument();

    });
  
    it("exibe mensagem de erro ao enviar formulário com o padrão errado no campo de série da turma", async () => {
      render(
        <BrowserRouter>
            <FormularioTurma/>
        </BrowserRouter>
      );
  
      const serie = screen.getByLabelText(/Série:/i);
      fireEvent.change(serie, { target: { value: "a" } });
  
      const botao = screen.getByText(/Finalizar/i)
      fireEvent.click(botao);
  
      expect(await screen.findByText("A série deve ser uma letra (A-Z)")).toBeInTheDocument();
      
    });

    
    it("valida que o ano deve ser igual ou maior que o ano atual", async () => {
        const anoAtual = new Date().getFullYear();
    
        render(
            <BrowserRouter>
                <FormularioTurma/>
            </BrowserRouter>
        );
    
        const input = screen.getByLabelText(/Ano Letivo:/i);
        fireEvent.change(input, { target: { value: 2024 } });

        const botao = screen.getByText(/Finalizar/i)
        fireEvent.click(botao);

        expect(await screen.findByText(new RegExp(`O ano deve ser igual ou maior que ${anoAtual}`, 'i'))).toBeInTheDocument();
    });
});