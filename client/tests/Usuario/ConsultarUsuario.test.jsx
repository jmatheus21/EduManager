import React from "react";
import { render, within, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import ConsultarUsuario from "../../src/pages/Usuario/ConsultarUsuario";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: '/usuario',
    search: '?success=false',
  }),
  useNavigate: jest.fn(),
}));

describe("ConsultarUsuario component", () => {

  it("renderiza os componentes corretamente", async () => {

    render(
      <BrowserRouter>
          <ConsultarUsuario />
      </BrowserRouter>
    );

    // Verifica se o título da página foi renderizado
    expect(await screen.getByText(/Consultar Usuários/i)).toBeInTheDocument();
  
    // Verifica se o campo foi renderizado
    expect(await screen.getByAllLabelText(/CPF:/i)).toBeInTheDocument(); // teste ai

    // expect(within(screen.getBy).getByText(/CPF/i)).toBeInTheDocument(); 
    expect(await screen.getByText(/Nome/i)).toBeInTheDocument();
    expect(await screen.getByText(/Tipo/i)).toBeInTheDocument();
    expect(await screen.getByText(/E-mail/i)).toBeInTheDocument();
    expect(await screen.getByText(/Telefone/i)).toBeInTheDocument(); 
    expect(await screen.getByText(/Data de Nascimento/i)).toBeInTheDocument();

    // Verifica se o botão foi renderizado
    expect(await screen.getByText(/Buscar/i)).toBeInTheDocument();
  });

  it("verifica se o usuário consegue digitar no campo de buscar", () => {

    render(
      <BrowserRouter>
        <ConsultarUsuario />
      </BrowserRouter>
    );

    const campoBuscar = screen.getByLabelText(/CPF:/i);
    fireEvent.change(campoBuscar, { target: { value: "111.111.111-11" }});

    fireEvent.click(screen.getByText(/Buscar/i));

    expect(campoBuscar.value).toBe("111.111.111-11");
  });
  
});