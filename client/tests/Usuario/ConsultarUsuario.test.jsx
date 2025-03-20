import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import  { ConsultarUsuario } from "../../src/pages/Usuario"

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
      pathname: "/usuario"
  }),
  useNavigate: jest.fn(),
}));

jest.mock("../../src/hooks/useApi", () => ({
  __esModule: true,
  default: () => ({
      fetchData: jest.fn().mockResolvedValue({ success: true }),
      loading: false,
      error: null,
      data: []
  })
}));

/**
 * Testes unitários para o componente ConsultarUsuario.
 * Verifica a renderização inicial, a interação do usuário e o carregamento de dados.
 */
describe("ConsultarUsuario", () => {

  beforeEach(() => {
      render(
          <BrowserRouter>
              <ConsultarUsuario/>
          </BrowserRouter>
      );
  })

  it ("renderiza o formulário corretamente", async () => {
      
      // Verifica se o título da página foi renderizado
      expect(screen.getByText(/Consultar Usuários/i)).toBeVisible();

      // // Verifica se o campo 'CPF' foi renderizado
      expect(screen.getByPlaceholderText("Exemplo: 999.888.777-66")).toBeVisible();

      // // Verifica se o botão foi renderizado
      expect(screen.getByText(/Buscar/i)).toBeVisible();

      // // Verifica se o campo 'CPF' foi renderizado
      expect(screen.getByRole("columnheader", { name: /CPF/i })).toBeVisible();   
      
      // // Verifica se o campo 'Nome' foi renderizado
      expect(screen.getByRole("columnheader", { name: /Nome/i })).toBeVisible();

      // // Verifica se o campo 'Tipo' foi renderizado
      expect(screen.getByRole("columnheader", { name: /Tipo/i })).toBeVisible();

      // // Verifica se o campo "E-mail" foi renderizado
      expect(screen.getByRole("columnheader", { name: /E-mail/i })).toBeVisible();

      // // Verifica se o campo 'Telefone' foi renderizado
      expect(screen.getByRole("columnheader", { name: /Telefone/i })).toBeVisible();

      // // Verifica se o campo 'Data de Nascimento' foi renderizado
      expect(screen.getByRole("columnheader", { name: /Data de Nascimento/i })).toBeVisible();
  });

  it ("verifica se é possível inserir dados no campo de busca", async () => {
      render(
          <BrowserRouter>
              <ConsultarUsuario/>
          </BrowserRouter>
      );

      const camposBusca = screen.getAllByPlaceholderText("Exemplo: 999.888.777-66");
      const campoBusca = camposBusca[0];

      await userEvent.type(campoBusca, "999.888.777-66");

      expect(campoBusca.value).toBe("999.888.777-66");
  });
});

