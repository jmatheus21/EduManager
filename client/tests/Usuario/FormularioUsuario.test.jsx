import React from "react";
import { render, within, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { FormularioUsuario } from "../../src/pages/Usuario"

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: jest.fn(),
  useNavigate: jest.fn(),
}));


/**
 * Testes unitários para o componente ConsultarUsuario.
 * Este conjunto de testes verifica a renderização correta do componente,
 * a interação com a barra de busca e a exibição de mensagens de sucesso/erro.
 */
describe("ConsultarUsuario Component", () => {

  it("renderiza o formulário corretamente para 'professor' e para 'funcionario", () => {

    
    render(
      <BrowserRouter>
        <FormularioUsuario/>
      </BrowserRouter>
    );

    expect(screen.getByText(/Cadastrar Usuário/i)).toBeInTheDocument();
    expect(within(screen.getByTestId('nome')).getByText(/Nome:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Email:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/CPF:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Data de Nascimento:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Tipo:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Horário de Trabalho:/i)).toBeInTheDocument();
    expect(within(screen.getByTestId('senha')).getByText("Senha:")).toBeInTheDocument();
    expect(screen.getByLabelText(/Confirmar senha:/i)).toBeInTheDocument();
    expect(screen.getByText(/Cargos/i)).toBeInTheDocument();
    expect(within(screen.getByTestId('nomeCargo')).getByText(/Nome:/i)).toBeInTheDocument();
    expect(within(screen.getByTestId('salarioCargo')).getByText("Salário Mensal (R$):")).toBeInTheDocument();
    expect(within(screen.getByTestId('dataContratoCargo')).getByText(/Data de contrato:/i)).toBeInTheDocument();

    expect(screen.getByLabelText(/Formação:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Código\(s\) da\(s\) Disciplinas:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Habilidades:/i).closest('.row')).toHaveClass('d-none');
    expect(screen.getByLabelText(/Escolaridade:/i).closest('.row')).toHaveClass('d-none');

    const tipoSelect = screen.getByRole('combobox', { name: /Tipo:/i });
    expect(tipoSelect).toBeInTheDocument();
  
    fireEvent.change(tipoSelect, { target: { value: 'f' } });
    expect(tipoSelect.value).toBe('f');

    expect(screen.getByLabelText(/Habilidades:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Escolaridade:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Formação:/i).closest('.row')).toHaveClass('d-none');
    expect(screen.getByLabelText(/Código\(s\) da\(s\) Disciplinas:/i).closest('.row')).toHaveClass('d-none');
  })

  it("exibe mensagem de erro ao enviar formulário sem preencher campos obrigatórios", async () => {
    render(
      <BrowserRouter>
        <FormularioUsuario />
      </BrowserRouter>
    );

    fireEvent.click(screen.getByText(/Finalizar/i));

    expect(await screen.findByText(/O nome é obrigatório/i)).toBeInTheDocument();
    expect(await screen.findByText(/O e-mail é obrigatório/i)).toBeInTheDocument();
    expect(await screen.findByText(/O CPF é obrigatório/i)).toBeInTheDocument();
    expect(await screen.findByText(/A data de nascimento é obrigatória/i)).toBeInTheDocument();
    expect(await screen.findByText(/O horário de trabalho é obrigatório/i)).toBeInTheDocument();
    expect(await screen.findByText(/A senha é obrigatória/i)).toBeInTheDocument();
    expect(await screen.findByText(/A senha a ser confirmada é obrigatória/i)).toBeInTheDocument();
    expect(await screen.findByText(/A formação do professor é obrigatória/i)).toBeInTheDocument();
    expect(await screen.findByText(/As disciplinas do professor são obrigatórias/i)).toBeInTheDocument();

    const tipoSelect = screen.getByRole('combobox', { name: /Tipo:/i });
    fireEvent.change(tipoSelect, { target: { value: 'f' } });

    fireEvent.click(screen.getByText(/Finalizar/i));

    expect(await screen.findByText(/As habilidades do funcionário são obrigatórias/i)).toBeInTheDocument();
    expect(await screen.findByText(/A escolaridade do funcionário é obrigatória/i)).toBeInTheDocument();
  })

  it('permite ao usuário digitar no campo de nome', () => {
    render(
      <BrowserRouter>
        <FormularioUsuario />
      </BrowserRouter>
    );
    
    const nomeInput = screen.getByPlaceholderText(/Cristóvão Colombo/i);
    fireEvent.change(nomeInput, { target: { value: 'João Silva' } });
    
    const emailInput = screen.getByLabelText(/Email:/i);
    fireEvent.change(emailInput, { target: { value: 'jsilva@terra.com.br' } });
    
    const cpfInput = screen.getByLabelText(/CPF:/i);
    fireEvent.change(cpfInput, { target: { value: '999.888.777-66' } });
    
    const dataDeNascimentoInput = screen.getByLabelText(/Data de Nascimento:/i);
    fireEvent.change(dataDeNascimentoInput, { target: { value: '2000-06-27' } });
    
    const telefoneInput = screen.getByLabelText(/Telefone:/i);
    fireEvent.change(telefoneInput, { target: { value: '99 9 9879-1793' } });
    
    const horarioDeTrabalhoInput = screen.getByLabelText(/Horário de Trabalho:/i);
    fireEvent.change(horarioDeTrabalhoInput, { target: { value: 'Seg-Sex,8h-17h' } });
    
    const tipoInput = screen.getByLabelText(/Tipo:/i);
    fireEvent.change(tipoInput, { target: { value: 'p' } });
    
    const enderecoInput = screen.getByLabelText(/Endereço:/i);
    fireEvent.change(enderecoInput, { target: { value: 'Rua das Aves, N° 123' } });
    
    const senhaInput = screen.getByPlaceholderText(/No mínimo 5 caracteres/i);
    fireEvent.change(senhaInput, { target: { value: 'novaSenha' } });
    
    const confirmarSenhaInput = screen.getByLabelText(/Confirmar senha:/i);
    fireEvent.change(confirmarSenhaInput, { target: { value: 'novaSenha' } });
    
    const formacaoInput = screen.getByLabelText(/Formação:/i);
    fireEvent.change(formacaoInput, { target: { value: 'Bacharelado em Matemática' } });
    
    const codigosDisciplinasInput = screen.getByLabelText(/Código\(s\) da\(s\) Disciplinas:/i);
    fireEvent.change(codigosDisciplinasInput, { target: { value: 'MAT101,FIS789' } });
    
    expect(nomeInput.value).toBe('João Silva');
    expect(emailInput.value).toBe('jsilva@terra.com.br');
    expect(cpfInput.value).toBe('999.888.777-66');
    expect(dataDeNascimentoInput.value).toBe('2000-06-27');
    expect(telefoneInput.value).toBe('99 9 9879-1793');
    expect(horarioDeTrabalhoInput.value).toBe('Seg-Sex,8h-17h');
    expect(tipoInput.value).toBe('p');
    expect(enderecoInput.value).toBe('Rua das Aves, N° 123');
    expect(senhaInput.value).toBe('novaSenha');
    expect(confirmarSenhaInput.value).toBe('novaSenha');
    expect(formacaoInput.value).toBe('Bacharelado em Matemática');
    expect(codigosDisciplinasInput.value).toBe('MAT101,FIS789');

    fireEvent.change(tipoInput, { target: { value: 'f' } }); 

    const habilidadesInput = screen.getByLabelText(/Habilidades:/i);
    fireEvent.change(habilidadesInput, { target: { value: "Informática básica" } });
    
    const escolaridadeInput = screen.getByLabelText(/Escolaridade:/i);
    fireEvent.change(escolaridadeInput, { target: { value: "Ensino superior completo" } });
  });
})