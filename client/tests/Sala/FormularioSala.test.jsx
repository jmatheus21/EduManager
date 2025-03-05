import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter as Router, useLocation, useParams } from "react-router";
import FormularioSala from "../../src/pages/Sala/FormularioSala";
import useApi from "../../src/hooks/useApi";

// Mock do useApi
jest.mock("../src/hooks/useApi", () => ({
  __esModule: true,
  default: jest.fn(),
}));

// Mock do useLocation e useParams
jest.mock("react-router", () => ({
  ...jest.requireActual("react-router"),
  useLocation: jest.fn(),
  useParams: jest.fn(),
}));

/**
 * Testes unitários para o componente FormularioSala.
 * Este conjunto de testes verifica a renderização correta do componente,
 * a interação com o formulário e a exibição de mensagens de erro.
 */
describe("FormularioSala Component", () => {
  const mockFetchData = jest.fn();
  const mockCreateData = jest.fn();
  const mockUpdateData = jest.fn();
  const mockNavigate = jest.fn();

  beforeEach(() => {
    // Mock do useApi
    useApi.mockReturnValue({
      loading: false,
      error: null,
      data: null,
      fetchData: mockFetchData,
      createData: mockCreateData,
      updateData: mockUpdateData,
    });

    // Mock do useLocation
    useLocation.mockReturnValue({
      pathname: "/cadastrar",
    });

    // Mock do useParams
    useParams.mockReturnValue({});
  });

  /**
   * Verifica se o componente é renderizado corretamente no modo de cadastro.
   */
  it("deve renderizar o componente no modo de cadastro", () => {
    render(
      <Router>
        <FormularioSala />
      </Router>
    );

    // Verifica se o título está presente
    expect(screen.getByText("Cadastrar Sala")).toBeInTheDocument();

    // Verifica se os campos do formulário estão presentes
    expect(screen.getByLabelText("Número:")).toBeInTheDocument();
    expect(screen.getByLabelText("Capacidade:")).toBeInTheDocument();
    expect(screen.getByLabelText("Localização:")).toBeInTheDocument();

    // Verifica se o botão de cadastro está presente
    expect(screen.getByRole("button", { name: /Finalizar/i })).toBeInTheDocument();
  });

  /**
   * Verifica se o componente é renderizado corretamente no modo de alteração.
   */
  it("deve renderizar o componente no modo de alteração", async () => {
    // Mock do useLocation para simular a rota de alteração
    useLocation.mockReturnValue({
      pathname: "/alterar/101",
    });

    // Mock do useParams para simular o parâmetro da URL
    useParams.mockReturnValue({
      numeroParam: "101",
    });

    // Mock do fetchData para retornar dados da sala existente
    mockFetchData.mockResolvedValue({
      numero: 101,
      capacidade: 50,
      localizacao: "Bloco A",
    });

    render(
      <Router>
        <FormularioSala />
      </Router>
    );

    // Aguarda o carregamento dos dados da sala
    await waitFor(() => {
      expect(screen.getByLabelText("Número:").value).toBe("101");
      expect(screen.getByLabelText("Capacidade:").value).toBe("50");
      expect(screen.getByLabelText("Localização:").value).toBe("Bloco A");
    });

    // Verifica se o título está presente
    expect(screen.getByText("Alterar Sala")).toBeInTheDocument();
  });

  /**
   * Verifica se o formulário é enviado corretamente no modo de cadastro.
   */
  it("deve enviar o formulário no modo de cadastro", async () => {
    render(
      <Router>
        <FormularioSala />
      </Router>
    );

    const inputNumero = screen.getByLabelText("Número:");
    const inputCapacidade = screen.getByLabelText("Capacidade:");
    const inputLocalizacao = screen.getByLabelText("Localização:");
    const botaoCadastrar = screen.getByRole("button", { name: /Finalizar/i });

    // Simula a entrada de dados
    fireEvent.change(inputNumero, { target: { value: "101" } });
    fireEvent.change(inputCapacidade, { target: { value: "50" } });
    fireEvent.change(inputLocalizacao, { target: { value: "Bloco A" } });

    // Simula o envio do formulário
    fireEvent.click(botaoCadastrar);

    // Verifica se a função createData foi chamada com os dados corretos
    await waitFor(() => {
      expect(mockCreateData).toHaveBeenCalledWith("/sala", {
        numero: 101,
        capacidade: 50,
        localizacao: "Bloco A",
      });
    });
  });

  // /**
  //  * Verifica se o formulário é enviado corretamente no modo de alteração.
  //  */
  // it("deve enviar o formulário no modo de alteração", async () => {
  //   // Mock do useLocation para simular a rota de alteração
  //   useLocation.mockReturnValue({
  //     pathname: "/alterar/101",
  //   });

  //   // Mock do useParams para simular o parâmetro da URL
  //   useParams.mockReturnValue({
  //     numeroParam: "101",
  //   });

  //   // Mock do fetchData para retornar dados da sala existente
  //   mockFetchData.mockResolvedValue({
  //     numero: 101,
  //     capacidade: 50,
  //     localizacao: "Bloco A",
  //   });

  //   render(
  //     <Router>
  //       <FormularioSala />
  //     </Router>
  //   );

  //   // Aguarda o carregamento dos dados da sala
  //   await waitFor(() => {
  //     expect(screen.getByLabelText("Número:").value).toBe("101");
  //     expect(screen.getByLabelText("Capacidade:").value).toBe("50");
  //     expect(screen.getByLabelText("Localização:").value).toBe("Bloco A");
  //   });

  //   const inputCapacidade = screen.getByLabelText("Capacidade:");
  //   const botaoCadastrar = screen.getByRole("button", { name: /Alterar/i });

  //   // Simula a alteração da capacidade
  //   fireEvent.change(inputCapacidade, { target: { value: "60" } });

  //   // Simula o envio do formulário
  //   fireEvent.click(botaoCadastrar);

  //   // Verifica se a função updateData foi chamada com os dados corretos
  //   await waitFor(() => {
  //     expect(mockUpdateData).toHaveBeenCalledWith("/sala/101", {
  //       numero: 101,
  //       capacidade: 60,
  //       localizacao: "Bloco A",
  //     });
  //   });
  // });

  /**
   * Verifica se as mensagens de erro são exibidas corretamente.
   */
  it("deve exibir mensagens de erro ao enviar o formulário com dados inválidos", async () => {
    // Mock do createData para simular um erro
    mockCreateData.mockRejectedValueOnce(new Error("Erro ao cadastrar sala"));

    render(
      <Router>
        <FormularioSala />
      </Router>
    );

    const inputNumero = screen.getByLabelText("Número:");
    const inputCapacidade = screen.getByLabelText("Capacidade:");
    const inputLocalizacao = screen.getByLabelText("Localização:");
    const botaoCadastrar = screen.getByRole("button", { name: /Finalizar/i });

    // Simula a entrada de dados
    fireEvent.change(inputNumero, { target: { value: "101" } });
    fireEvent.change(inputCapacidade, { target: { value: "50" } });
    fireEvent.change(inputLocalizacao, { target: { value: "Bloco A" } });

    // Simula o envio do formulário
    fireEvent.click(botaoCadastrar);

    // Aguarda a exibição da mensagem de erro
    await waitFor(() => {
      expect(screen.getByText("Erro ao cadastrar sala")).toBeInTheDocument();
    });
  });
});