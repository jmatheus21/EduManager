import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter as Router, useLocation, useNavigate } from "react-router";
import ConsultarSala from "../../src/pages/Sala/ConsultarSala";
import useApi from "../../src/hooks/useApi";

// Mock do useApi
jest.mock("../src/hooks/useApi", () => ({
  __esModule: true,
  default: jest.fn(),
}));

// Mock do useLocation e useNavigate
jest.mock("react-router", () => ({
  ...jest.requireActual("react-router"),
  useLocation: jest.fn(),
  useNavigate: jest.fn(),
}));

/**
 * Testes unitários para o componente ConsultarSala.
 * Este conjunto de testes verifica a renderização correta do componente,
 * a interação com a barra de busca e a exibição de mensagens de sucesso/erro.
 */
describe("ConsultarSala Component", () => {
  const mockFetchData = jest.fn();
  const mockFetchDataBusca = jest.fn();
  const mockNavigate = jest.fn();

  beforeEach(() => {
    // Mock do useApi
    useApi.mockImplementation((baseUrl) => {
      if (baseUrl === "/api") {
        return {
          loading: false,
          error: null,
          data: [
            { numero: 1, capacidade: 20, localizacao: "Bloco A" },
            { numero: 2, capacidade: 30, localizacao: "Bloco B" },
          ],
          fetchData: mockFetchData,
        };
      } else if (baseUrl === "/apiBusca") {
        return {
          loading: false,
          error: null,
          data: null,
          fetchData: mockFetchDataBusca,
        };
      }
    });

    // Mock do useLocation
    useLocation.mockReturnValue({
      pathname: "/consultar-sala",
      search: "",
    });

    // Mock do useNavigate
    useNavigate.mockReturnValue(mockNavigate);
  });

  /**
   * Verifica se o componente é renderizado corretamente com as colunas e dados esperados.
   */
  it("deve renderizar o componente com as colunas e dados corretos", () => {
    render(
      <Router>
        <ConsultarSala />
      </Router>
    );

    // Verifica se o título está presente
    expect(screen.getByText("Consultar Salas")).toBeInTheDocument();

    // Verifica se as colunas estão presentes
    expect(screen.getByText("Número")).toBeInTheDocument();
    expect(screen.getByText("Capacidade")).toBeInTheDocument();
    expect(screen.getByText("Localização")).toBeInTheDocument();

    // Verifica se os dados estão presentes
    expect(screen.getByText("1")).toBeInTheDocument();
    expect(screen.getByText("20")).toBeInTheDocument();
    expect(screen.getByText("Bloco A")).toBeInTheDocument();
    expect(screen.getByText("2")).toBeInTheDocument();
    expect(screen.getByText("30")).toBeInTheDocument();
    expect(screen.getByText("Bloco B")).toBeInTheDocument();
  });

  /**
   * Verifica se a barra de busca é renderizada corretamente.
   */
  it("deve renderizar a barra de busca com os atributos corretos", () => {
    render(
      <Router>
        <ConsultarSala />
      </Router>
    );

    // Verifica se a barra de busca está presente
    expect(screen.getByLabelText("Número:")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Exemplo: 10")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Buscar/i })).toBeInTheDocument();
  });

  /**
   * Verifica se a função de busca é chamada corretamente ao clicar no botão de busca.
   */
  it("deve chamar a função de busca ao clicar no botão de busca", async () => {
    render(
      <Router>
        <ConsultarSala />
      </Router>
    );

    const inputNumero = screen.getByPlaceholderText("Exemplo: 10");
    const botaoBuscar = screen.getByRole("button", { name: /Buscar/i });

    // Simula a entrada de um número e o clique no botão de busca
    fireEvent.change(inputNumero, { target: { value: "5" } });
    fireEvent.click(botaoBuscar);

    // Verifica se a função de busca foi chamada
    await waitFor(() => {
      expect(mockFetchData).toHaveBeenCalledWith("/sala/5");
    });
  });

  /**
   * Verifica se a mensagem de sucesso é exibida corretamente quando o parâmetro 'success' está presente na URL.
   */
  it("deve exibir uma mensagem de sucesso quando o parâmetro 'success' está presente na URL", () => {
    // Mock do useLocation para simular a presença do parâmetro 'success'
    useLocation.mockReturnValue({
      pathname: "/consultar-sala",
      search: "?success=true&type=cadastro",
    });

    render(
      <Router>
        <ConsultarSala />
      </Router>
    );

    // Verifica se a mensagem de sucesso está presente
    expect(screen.getByText("Sala cadastrada com sucesso!")).toBeInTheDocument();
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
        <ConsultarSala />
      </Router>
    );

    // Verifica se a mensagem de carregamento está presente
    expect(screen.getByText("Carregando...")).toBeInTheDocument();
  });
});