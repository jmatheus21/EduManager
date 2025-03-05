import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { BarraDeBusca } from "../../src/components"

/**
 * Testes unitários para o componente BarraDeBusca.
 * Este conjunto de testes verifica a renderização correta do componente,
 * a interação com os campos de busca e a chamada das funções passadas como props.
 */

describe("BarraDeBusca Component", () => {
  /**
   * Verifica se o componente é renderizado corretamente com as props fornecidas.
   */
  it("deve renderizar o componente com o atributo nome e placeholder corretos", () => {
    const mockFuncaoAlteracao = jest.fn();
    const mockFuncaoBotao = jest.fn();

    render(
      <BarraDeBusca
        atributoNome="Nome"
        tipo="text"
        placeholder="Digite o nome"
        minLength={3}
        maxLength={10}
        funcaoAlteracao={mockFuncaoAlteracao}
        funcaoBotao={mockFuncaoBotao}
      />
    );

    // Verifica se o rótulo e o campo de busca estão presentes
    expect(screen.getByText(/Nome:/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Digite o nome/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Buscar/i })).toBeInTheDocument();
  });

  /**
   * Verifica se a função de alteração é chamada corretamente ao digitar no campo de busca.
   */
  it("deve chamar a função de alteração ao digitar no campo de busca", () => {
    const mockFuncaoAlteracao = jest.fn();
    const mockFuncaoBotao = jest.fn();

    render(
      <BarraDeBusca
        atributoNome="Nome"
        tipo="text"
        placeholder="Digite o nome"
        minLength={3}
        maxLength={10}
        funcaoAlteracao={mockFuncaoAlteracao}
        funcaoBotao={mockFuncaoBotao}
      />
    );

    const inputField = screen.getByPlaceholderText(/Digite o nome/i);
    fireEvent.change(inputField, { target: { value: "marcos" } });

    // Verifica se a função foi chamada com o valor correto
    expect(mockFuncaoAlteracao).toHaveBeenCalledWith("marcos");
  });

  /**
   * Verifica se a função do botão é chamada corretamente ao clicar no botão de busca.
   */
  it("deve chamar a função do botão ao clicar no botão de busca", () => {
    const mockFuncaoAlteracao = jest.fn();
    const mockFuncaoBotao = jest.fn();

    render(
      <BarraDeBusca
        atributoNome="Número"
        tipo="text"
        placeholder="Digite o número"
        minLength={3}
        maxLength={10}
        funcaoAlteracao={mockFuncaoAlteracao}
        funcaoBotao={mockFuncaoBotao}
      />
    );

    const botaoBuscar = screen.getByRole("button", { name: /Buscar/i });
    fireEvent.click(botaoBuscar);

    // Verifica se a função do botão foi chamada
    expect(mockFuncaoBotao).toHaveBeenCalled();
  });
});