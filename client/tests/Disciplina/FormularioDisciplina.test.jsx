import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import  { FormularioDisciplina } from "../../src/pages/Disciplina"

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: jest.fn(),
  useNavigate: jest.fn(),
}));

/**
 * Testes unitários para o componente FormularioDisciplina.
 * Este conjunto de testes verifica a renderização correta do componente
 * e a exibição de mensagens de sucesso/erro.
 */
describe("ConsultarUsuario Component", () => {
  it("renderiza o formulário corretamente", () => {
    render(
        <BrowserRouter>
            <FormularioDisciplina/>
        </BrowserRouter>
    );

    // Verifica se o título da página foi renderizado
    expect(screen.getByText(/Cadastrar Disciplina/i)).toBeInTheDocument();

    // Verifica se o campo "Nome:" foi renderizado
    expect(screen.getByLabelText(/Nome:/i)).toBeInTheDocument();

    // Verifica se o campo "Código:" foi renderizado
    expect(screen.getByLabelText(/Código:/i)).toBeInTheDocument();

    // Verifica se o campo "Carga Horária:" foi renderizado
    expect(screen.getByLabelText(/Carga Horária:/i)).toBeInTheDocument();

    // Verifica se o campo "Ementa:" foi renderizado
    expect(screen.getByLabelText(/Ementa:/i)).toBeInTheDocument();

    // Verifica se o campo "Bibliografia" foi renderizado
    expect(screen.getByLabelText(/Bibliografia:/i)).toBeInTheDocument();

    // Verifica se o botão foi renderizado
    expect(screen.getByText(/Finalizar/i)).toBeInTheDocument();
  });

  it("exibe mensagem de erro ao enviar formulário sem preencher campos obrigatórios", async () => {
    render(
        <BrowserRouter>
            <FormularioDisciplina/>
        </BrowserRouter>
    );

    // Clica no botão de finalizar sem preencher os campos obrigatórios
    const botao = screen.getByText(/Finalizar/i)
    fireEvent.click(botao);

    // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
    expect(await screen.findByText(/O nome da disciplina é obrigatório/i)).toBeInTheDocument();

    expect(await screen.findByText(/O código da disciplina é obrigatório/i)).toBeInTheDocument();

    expect(await screen.findByText(/A carga horária é obrigatória/i)).toBeInTheDocument();
  });

  it("permite ao usuário digitar nos campos do formulário", () => {
    render(
        <BrowserRouter>
            <FormularioDisciplina/>
        </BrowserRouter>
    );

    // busca o campo de código e simula a digitação de um nome
    const nomeInput = screen.getByLabelText(/Nome:/i);
    fireEvent.change(nomeInput, { target: { value: "Matemática" } });

    // exemplo com tipo código
    const codigoInput = screen.getByLabelText(/Código:/i);
    fireEvent.change(codigoInput, { target: { value: "MAT001" } });

    // exemplo com tipo number
    const cargaHorariaInput = screen.getByLabelText(/Carga Horária:/i);
    fireEvent.change(cargaHorariaInput, { target: { value: 30 } });

    // exemplo com tipo text
    const ementaInput = screen.getByLabelText(/Ementa:/i);
    fireEvent.change(ementaInput, { target: { value: "Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos." } });

    // exemplo com tipo text
    const bibliografiaInput = screen.getByLabelText(/Bibliografia:/i);
    fireEvent.change(bibliografiaInput, { target: { value: "STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014." } });
    
    // verifica se o dado foi digitado corretamente
    expect(nomeInput.value).toBe("Matemática");
    expect(codigoInput.value).toBe("MAT001");
    expect(cargaHorariaInput.value).toBe("30");
    expect(ementaInput.value).toBe("Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.");
    expect(bibliografiaInput.value).toBe("STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014."); 
  });

  it("exibe mensagem de erro ao enviar formulário com o número de caracteres menor do que o mínimo", async () => {
    render(
        <BrowserRouter>
            <FormularioDisciplina/>
        </BrowserRouter>
    );

    const nomeInput = screen.getByLabelText(/Nome:/i);
    fireEvent.change(nomeInput, { target: { value: "Ma" } });

    const codigoInput = screen.getByLabelText(/Código:/i);
    fireEvent.change(codigoInput, { target: { value: "MAT01" } });

    const cargaHorariaInput = screen.getByLabelText(/Carga Horária:/i);
    fireEvent.change(cargaHorariaInput, { target: { value: "10" } });

    // Clica no botão de finalizar com o número de caracteres menor do que o mínimo em algum campo
    const botao = screen.getByText(/Finalizar/i)
    fireEvent.click(botao);

    // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
    expect(await screen.findByText(/O nome da disciplina deve ter no mínimo 3 caracteres/i)).toBeInTheDocument();

    expect(await screen.findByText(/O código da disciplina deve ter no mínimo 6 caracteres/i)).toBeInTheDocument();

    expect(await screen.findByText(/A carga horária deve ser de no mínimo 15/i)).toBeInTheDocument();
  });

  it("exibe mensagem de erro ao enviar formulário com o número de caracteres maior do que o máximo", async () => {
    
    render(
      <BrowserRouter>
          <FormularioDisciplina/>
      </BrowserRouter>
    );

    const nomeInput = screen.getByLabelText(/Nome:/i);
    fireEvent.change(nomeInput, { target: { value: "MatemáticaMatemáticaMatemáticaMatemáticaMatemáticaMatemáticaMatemáticaMatemática" } });

    // exemplo com tipo código
    const codigoInput = screen.getByLabelText(/Código:/i);
    fireEvent.change(codigoInput, { target: { value: "MAT001MAT001" } });

    // exemplo com tipo number
    const cargaHorariaInput = screen.getByLabelText(/Carga Horária:/i);
    fireEvent.change(cargaHorariaInput, { target: { value: "160" } });

    // exemplo com tipo select
    const ementaInput = screen.getByLabelText(/Ementa:/i);
    fireEvent.change(ementaInput, { target: { value: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" } });

    // exemplo com tipo select
    const bibliografiaInput = screen.getByLabelText(/Bibliografia:/i);
    fireEvent.change(bibliografiaInput, { target: { value: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" } });
  
    // Clica no botão de finalizar com número de caracteres maior do que o máximo permitido
    const botao = screen.getByText(/Finalizar/i)
    fireEvent.click(botao);

    // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
    expect(await screen.findByText(/O nome da disciplina deve ter no máximo 50 caracteres/i)).toBeInTheDocument();
    
    expect(await screen.findByText(/O código da disciplina deve ter no máximo 10 caracteres/i)).toBeInTheDocument();
    
    expect(await screen.findByText(/A carga horária deve ser no máximo 120/i)).toBeInTheDocument();
    
    expect(await screen.findByText(/A ementa deve ter no máximo 255 caracteres/i)).toBeInTheDocument();
    
    expect(await screen.findByText(/A bibliografia deve ter no máximo 255 caracteres/i)).toBeInTheDocument();
  });

  it("exibe mensagem de erro ao enviar formulário com o padrão errado no campo de código da disciplina", async () => {
    render(
      <BrowserRouter>
          <FormularioDisciplina/>
      </BrowserRouter>
    );

    const codigo = screen.getByLabelText(/Código:/i);
    fireEvent.change(codigo, { target: { value: "123MAT" } });

    const botao = screen.getByText(/Finalizar/i)
    fireEvent.click(botao);

    expect(await screen.findByText("O código da disciplina não está no formato correto. Utilize três letras maiúsculas seguidas de três números (ex: MAT123)")).toBeInTheDocument();
    
  });
});