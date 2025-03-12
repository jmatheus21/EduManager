import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import FormularioCalendario from "../../src/pages/Calendario/FormularioCalendario";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: jest.fn(),
  useNavigate: jest.fn(),
}));

const anoAtual = new Date().getFullYear();

/**
 * Testes unitários para o componente FormularioCalendario.
 * Este conjunto de testes verifica a renderização correta do componente,
 * a interação com a barra de busca e a exibição de mensagens de sucesso/erro.
 */
describe("FormularioCalendario Component", () => {
  it("renderiza o formulário corretamente", () => {
    render(
      <BrowserRouter>
        <FormularioCalendario/>
      </BrowserRouter>
    );

    // Verifica se o título da página foi renderizado
    expect(screen.getByText(/Cadastrar Calendário/i)).toBeInTheDocument();

    // Verifica se cada campo foi renderizado
    expect(screen.getByLabelText(/Ano letivo:/i)).toBeInTheDocument();

    expect(screen.getByLabelText(/Data de início/i)).toBeInTheDocument();

    expect(screen.getByLabelText(/Dias letivos:/i)).toBeInTheDocument();
    
    expect(screen.getByLabelText(/Data de fim:/i)).toBeInTheDocument();

    // Verifica se o botão foi renderizado
    expect(screen.getByText(/Finalizar/i)).toBeInTheDocument();

    /*
      expect = verifica se a condição é verdadeira
      screen.getByText = busca um elemento na tela com o texto passado como parâmetro
      /Cadastrar Entidade/i = expressão regular que busca o texto "Cadastrar Entidade" ignorando maiúsculas e minúsculas
      screen.getByLabelText = busca um campo de formulário na tela pelo texto da label
    */
  });
  
  it("exibe mensagem de erro ao enviar formulário sem preencher campos obrigatórios", async () => {
    render(<BrowserRouter>{<FormularioCalendario/>}</BrowserRouter>);

    // Clica no botão de finalizar sem preencher os campos obrigatórios
    fireEvent.click(screen.getByText(/Finalizar/i));

    // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
    expect(await screen.findByText(/O ano letivo é obrigatório/i)).toBeInTheDocument();
    expect(await screen.findByText(/A quantidade de dias letivos é obrigatória/i)).toBeInTheDocument();
    expect(await screen.findByText(/A data de início é obrigatória/i)).toBeInTheDocument();
    expect(await screen.findByText(/A data de fim é obrigatória/i)).toBeInTheDocument();
  });

  it("exibe mensagens de erro ao enviar formulário com dados inválidos (ano letivo, dias letivos, data de início, data de fim)", async () => {
    render(<BrowserRouter>{<FormularioCalendario/>}</BrowserRouter>); 
    
    //Inserção de dados inválidos e contraditórios
    const anoLetivoInput = screen.getByLabelText(/Ano letivo:/i);
    fireEvent.change(anoLetivoInput, { target: { value: 2024 } });

    const diasLetivosInput = screen.getByLabelText(/Dias letivos:/i);
    fireEvent.change(diasLetivosInput, { target: { value: 208 } });

    const dataInicioInput = screen.getByLabelText(/Data de início:/i);
    fireEvent.change(dataInicioInput, { target: { value: "2026-01-15" } });

    const dataFimInput = screen.getByLabelText(/Data de fim:/i);
    fireEvent.change(dataFimInput, { target: { value: "2026-01-09" } });
    
    // Clica no botão de finalizar sem preencher os campos obrigatórios
    fireEvent.click(screen.getByText(/Finalizar/i));

    // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
    expect(await screen.findByText(new RegExp(`O ano deve ser igual ou maior que ${anoAtual}`, 'i'))).toBeInTheDocument();
    expect(await screen.findByText(/A quantidade de dias letivos deve ser no máximo 200/i)).toBeInTheDocument();
    expect(await screen.findByText(/A data de início deve ser no mesmo ano letivo inserido/i)).toBeInTheDocument();
    expect(await screen.findByText(/A data de fim é anterior à data de início ou ela não pertence ao mesmo ano letivo/i)).toBeInTheDocument();
    
  });

  it("permite ao usuário digitar nos campos do formulário", () => {
    render(<BrowserRouter>{<FormularioCalendario/>}</BrowserRouter>);

    //Inserção de dados válidos
    const anoLetivoInput = screen.getByLabelText(/Ano letivo:/i);
    fireEvent.change(anoLetivoInput, { target: { value: 2026 } });

    const diasLetivosInput = screen.getByLabelText(/Dias letivos:/i);
    fireEvent.change(diasLetivosInput, { target: { value: 150 } });

    const dataInicioInput = screen.getByLabelText(/Data de início:/i);
    fireEvent.change(dataInicioInput, { target: { value: "2026-01-15" } });

    const dataFimInput = screen.getByLabelText(/Data de fim:/i);
    fireEvent.change(dataFimInput, { target: { value: "2026-09-15" } });

    // verifica se o dado foi digitado corretamente
    expect(anoLetivoInput.value).toBe("2026");
    expect(diasLetivosInput.value).toBe("150"); 
    expect(dataInicioInput.value).toBe("2026-01-15");
    expect(dataFimInput.value).toBe("2026-09-15");
  });
  
});

