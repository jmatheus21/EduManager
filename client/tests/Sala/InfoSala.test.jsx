import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter as Router, useParams, useLocation } from "react-router";
import InfoSala from "../../src/pages/Sala/InfoSala";
import useApi from "../../src/hooks/useApi";

// Mock do useApi
jest.mock("../src/hooks/useApi", () => ({
  __esModule: true,
  default: jest.fn(),
}));

// Mock do useParams e useLocation
jest.mock("react-router", () => ({
  ...jest.requireActual("react-router"),
  useParams: jest.fn(),
  useLocation: jest.fn(),
}));

/**
 * Testes unitários para o componente InfoSala.
 * Este conjunto de testes verifica a renderização correta do componente,
 * o carregamento de dados, a exibição de mensagens de sucesso e a interação com o modal de remoção.
 */
describe("InfoSala Component", () => {
  const mockFetchData = jest.fn();
  const mockDeleteData = jest.fn();

  beforeEach(() => {
    // Mock do useApi
    useApi.mockReturnValue({
      loading: false,
      error: null,
      data: { numero: 101, capacidade: 50, localizacao: "Bloco A" },
      fetchData: mockFetchData,
      deleteData: mockDeleteData,
    });

    // Mock do useParams
    useParams.mockReturnValue({
      numero: "101",
    });

    // Mock do useLocation
    useLocation.mockReturnValue({
      search: "",
    });
  });

  /**
   * Verifica se o componente é renderizado corretamente com os dados da sala.
   */
  it("deve renderizar o componente com os dados da sala", () => {
    render(
      <Router>
        <InfoSala />
      </Router>
    );

    // Verifica se o título está presente
    expect(screen.getByText("Informações da Sala")).toBeInTheDocument();

    // Verifica se os dados da sala estão presentes
    expect(screen.getByText("101")).toBeInTheDocument();
    expect(screen.getByText("50")).toBeInTheDocument();
    expect(screen.getByText("Bloco A")).toBeInTheDocument();
  });

  /**
   * Verifica se a mensagem de sucesso é exibida corretamente quando o parâmetro 'success' está presente na URL.
   */
  it("deve exibir uma mensagem de sucesso quando o parâmetro 'success' está presente na URL", () => {
    // Mock do useLocation para simular a presença do parâmetro 'success'
    useLocation.mockReturnValue({
      search: "?success=true",
    });

    render(
      <Router>
        <InfoSala />
      </Router>
    );

    // Verifica se a mensagem de sucesso está presente
    expect(screen.getByText("Sala alterada com sucesso!")).toBeInTheDocument();
  });

  /**
   * Verifica se o modal de remoção é aberto corretamente ao clicar no botão de remover.
   */
  it("deve abrir o modal de remoção ao clicar no botão de remover", () => {
    render(
      <Router>
        <InfoSala />
      </Router>
    );

    const botaoRemover = screen.getByRole("button", { name: /Remover/i });
    fireEvent.click(botaoRemover);

    // Verifica se o modal está aberto
    expect(screen.getByText("Remover Sala")).toBeInTheDocument();
  });

  /**
   * Verifica se a função de remoção é chamada corretamente ao confirmar a remoção no modal.
   */
  it("deve chamar a função de remoção ao confirmar a remoção no modal", async () => {
    render(
      <Router>
        <InfoSala />
      </Router>
    );

    const botaoRemover = screen.getByRole("button", { name: /Remover/i });
    fireEvent.click(botaoRemover);

    const botaoConfirmarRemocao = screen.getByRole("button", { name: /Confirmar/i });
    fireEvent.click(botaoConfirmarRemocao);

    // Verifica se a função deleteData foi chamada
    await waitFor(() => {
      expect(mockDeleteData).toHaveBeenCalledWith("/sala/101");
    });
  });

  /**
   * Verifica se a mensagem de carregamento é exibida corretamente enquanto os dados estão sendo buscados.
   */
  it("deve exibir uma mensagem de carregamento enquanto os dados estão sendo buscados", () => {
    // Mock do useApi para simular o estado de carregamento
    useApi.mockReturnValue({
      loading: true,
      error: null,
      data: null,
      fetchData: mockFetchData,
    });

    render(
      <Router>
        <InfoSala />
      </Router>
    );

    // Verifica se a mensagem de carregamento está presente
    expect(screen.getByText("Carregando...")).toBeInTheDocument();
  });

  /**
   * Verifica se a mensagem de erro é exibida corretamente caso ocorra um erro na requisição.
   */
  it("deve exibir uma mensagem de erro caso ocorra um erro na requisição", () => {
    // Mock do useApi para simular um erro
    useApi.mockReturnValue({
      loading: false,
      error: "Erro ao carregar dados",
      data: null,
      fetchData: mockFetchData,
    });

    render(
      <Router>
        <InfoSala />
      </Router>
    );

    // Verifica se a mensagem de erro está presente
    expect(screen.getByText("Erro: Erro ao carregar dados")).toBeInTheDocument();
  });
});