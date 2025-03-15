import React from "react";
import { render, screen, fireEvent, waitFor, act, within, logRoles } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { FormularioUsuario } from "../../src/pages/Usuario"
import Formulario from "../../src/pages/Usuario/components/Formulario";


// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/usuario"
  }),
  useNavigate: jest.fn(),
}));


/**
 * Testes unitários para o componente FormularioUsuario.
 * Este conjunto de testes verifica a renderização correta do componente,
 * a interação com a barra de busca e a exibição de mensagens de sucesso/erro.
 */
describe("FormulariorUsuario Component", () => {

  describe("Teste de cadastrar usuário", () => {
    
    beforeEach(() => {
      render(
        <BrowserRouter>
                <FormularioUsuario/>
            </BrowserRouter>
        );
    })

    it ("renderiza o formulário corretamente para 'professor' e para 'funcionario", () => {
  
      // Verifica se o título da página foi renderizado
      expect(screen.getByText(/Cadastrar Usuário/i)).toBeVisible();
      
      // Verifica se o campo 'Nome' foi renderizado
      expect(within(screen.getByTestId('nome')).getByText(/Nome:/i)).toBeVisible();
  
      // Verifica se o campo 'Email' foi renderizado
      expect(screen.getByLabelText(/Email:/i)).toBeVisible();
  
      // Verifica se o campo 'CPF' foi renderizado
      expect(screen.getByLabelText(/CPF:/i)).toBeVisible();
  
      // Verifica se o campo 'Data de nascimento' foi renderizado
      expect(screen.getByLabelText(/Data de Nascimento:/i)).toBeVisible();
      
      // Verifica se o campo 'Tipo de Trabalho' foi renderizado
      expect(screen.getByLabelText(/Tipo:/i)).toBeVisible();
  
      // Verifica se o campo 'Horário de Trabalho' foi renderizado
      expect(screen.getByLabelText(/Horário de Trabalho:/i)).toBeVisible();
  
      // Verifica se o campo 'Senha' foi renderizado
      expect(within(screen.getByTestId('senha')).getByText("Senha:")).toBeVisible();
  
      // Verifica se o campo 'Confirmar senha' foi renderizado
      expect(screen.getByLabelText(/Confirmar senha:/i)).toBeVisible();
  
      // Verifica se o fieldset 'Cargos' foi renderizado
      expect(screen.getByText(/Cargos/i)).toBeVisible();
  
      // Verifica se o campo 'Nome' do cargo foi renderizado
      expect(within(screen.getByTestId('nomeCargo')).getByText(/Nome:/i)).toBeVisible();
  
      // Verifica se o campo 'Salário Mensal (R$)' do cargo foi renderizado
      expect(within(screen.getByTestId('salarioCargo')).getByText("Salário Mensal (R$):")).toBeVisible();
  
      // Verifica se o campo 'Data de contrato' do cargo foi renderizado
      expect(within(screen.getByTestId('dataContratoCargo')).getByText(/Data de contrato:/i)).toBeVisible();
  
      // Verifica se o campo 'Formação' foi renderizado
      expect(screen.getByLabelText(/Formação:/i)).toBeVisible();
  
      // Verifica se o campo 'Código(s) da(s) Disciplinas' foi renderizado
      expect(screen.getByLabelText(/Código\(s\) da\(s\) Disciplinas:/i)).toBeVisible();
      
      // Verifica se o campo 'Habilidades' não foi renderizado
      expect(screen.getByLabelText(/Habilidades:/i).closest('.row')).toHaveClass('d-none');
  
      // Verifica se o campo 'Escolaridade' não foi renderizado
      expect(screen.getByLabelText(/Escolaridade:/i).closest('.row')).toHaveClass('d-none');
  
      // Verifica se o campo 'Tipo' foi renderizado
      const tipoSelect = screen.getByRole('combobox', { name: /Tipo:/i });
      expect(tipoSelect).toBeVisible();
    
      // Altera o tipo do usuário para funcionário
      fireEvent.change(tipoSelect, { target: { value: 'f' } });
      expect(tipoSelect.value).toBe('f'); 
  
      //Verifica se o campo 'Habilidades' foi renderizado
      expect(screen.getByLabelText(/Habilidades:/i)).toBeVisible();
  
      // Verifica se o campo 'Escolaridade' foi renderizado
      expect(screen.getByLabelText(/Escolaridade:/i)).toBeVisible();
  
      // Verifica se o campo 'Formação' não foi renderizado
      expect(screen.getByLabelText(/Formação:/i).closest('.row')).toHaveClass('d-none');
  
      // Verifica se o campo 'Código(s) da(s) Disciplinas' não foi renderizado
      expect(screen.getByLabelText(/Código\(s\) da\(s\) Disciplinas:/i).closest('.row')).toHaveClass('d-none');
    
    });

    it ("exibe mensagem de erro ao enviar formulário sem preencher campos obrigatórios", async () => {
  
      // Clica no botão de finalizar sem preencher os campos obrigatórios
      const botao = screen.getByText(/Finalizar/i);
      fireEvent.click(botao);
  
      // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
      expect(await screen.findByText(/O nome é obrigatório/i)).toBeVisible();
      expect(await screen.findByText(/O e-mail é obrigatório/i)).toBeVisible();
      expect(await screen.findByText(/O CPF é obrigatório/i)).toBeVisible();
      expect(await screen.findByText(/A data de nascimento é obrigatória/i)).toBeVisible();
      expect(await screen.findByText(/O telefone é obrigatório/i)).toBeVisible();
      expect(await screen.findByText(/O horário de trabalho é obrigatório/i)).toBeVisible();
      expect(await screen.findByText(/O endereço é obrigatório/i)).toBeVisible();
      expect(await screen.findByText(/A senha é obrigatória/i)).toBeVisible();
      expect(await screen.findByText(/A senha a ser confirmada é obrigatória/i)).toBeVisible();
      expect(await screen.findByText(/A formação do professor é obrigatória/i)).toBeVisible();
      expect(await screen.findByText(/As disciplinas do professor são obrigatórias/i)).toBeVisible();
  
      const tipoSelect = screen.getByRole('combobox', { name: /Tipo:/i });
      fireEvent.change(tipoSelect, { target: { value: 'f' } });
  
      fireEvent.click(screen.getByText(/Finalizar/i));
  
      expect(await screen.findByText(/As habilidades do funcionário são obrigatórias/i)).toBeVisible();
      expect(await screen.findByText(/A escolaridade do funcionário é obrigatória/i)).toBeVisible();
    })
    it ('permite ao usuário digitar nos campos do formulário', async () => {
  
      const nomeInput = screen.getByPlaceholderText(/Cristóvão Colombo/i);
      const emailInput = screen.getByLabelText(/Email:/i);
      const cpfInput = screen.getByLabelText(/CPF:/i);
      const dataDeNascimentoInput = screen.getByLabelText(/Data de Nascimento:/i);
      const telefoneInput = screen.getByLabelText(/Telefone:/i);
      const horarioDeTrabalhoInput = screen.getByLabelText(/Horário de Trabalho:/i);
      const tipoInput = screen.getByLabelText(/Tipo:/i);
      const enderecoInput = screen.getByLabelText(/Endereço:/i);
      const senhaInput = screen.getByPlaceholderText(/No mínimo 5 caracteres/i);
      const confirmarSenhaInput = screen.getByLabelText(/Confirmar senha:/i);
      const formacaoInput = screen.getByLabelText(/Formação:/i);
      const codigosDisciplinasInput = screen.getByLabelText(/Código\(s\) da\(s\) Disciplinas:/i);
     
      // realiza as ações
      await act(async () => {
        await userEvent.type(nomeInput, "João Silva");
        await userEvent.type(emailInput, "jsilva@email.com.br");
        await userEvent.type(cpfInput, "99988877766");
        await userEvent.type(dataDeNascimentoInput, "2004-09-01");
        await userEvent.type(telefoneInput, "99 9 9999-9999");
        await userEvent.type(horarioDeTrabalhoInput, "Seg-Sex,12h-17h");
        await userEvent.type(tipoInput, "p");
        await userEvent.type(enderecoInput, "Rua das Flores, N° 123");
        await userEvent.type(senhaInput, "senhaFacil");
        await userEvent.type(confirmarSenhaInput, "senhaFacil");
        await userEvent.type(formacaoInput, "Bacharelado em Matemática");
        await userEvent.type(codigosDisciplinasInput, "MAT101,FIS789");
      })
  
      // verifica se os dados foram digitados corretamente
      expect(nomeInput.value).toBe('João Silva');
      expect(emailInput.value).toBe('jsilva@email.com.br');
      expect(cpfInput.value).toBe('999.888.777-66');
      expect(dataDeNascimentoInput.value).toBe('2004-09-01');
      expect(telefoneInput.value).toBe('99 9 9999-9999');
      expect(horarioDeTrabalhoInput.value).toBe('Seg-Sex,12h-17h');
      expect(tipoInput.value).toBe('p');
      expect(enderecoInput.value).toBe('Rua das Flores, N° 123');
      expect(senhaInput.value).toBe('senhaFacil');
      expect(confirmarSenhaInput.value).toBe('senhaFacil');
      expect(formacaoInput.value).toBe('Bacharelado em Matemática');
      expect(codigosDisciplinasInput.value).toBe('MAT101,FIS789');
  
      fireEvent.change(tipoInput, { target: { value: 'f' } }); 
  
      const habilidadesInput = screen.getByLabelText(/Habilidades:/i);
      fireEvent.change(habilidadesInput, { target: { value: "Informática básica" } });
      
      const escolaridadeInput = screen.getByLabelText(/Escolaridade:/i);
      fireEvent.change(escolaridadeInput, { target: { value: "Ensino superior completo" } });
    });
  });

  describe("Teste de alterar usuário", () => {

    const mockEnviarFormulario = jest.fn();

    beforeEach(() => {
      render(
        <BrowserRouter>
          <Formulario enviarFormulario={mockEnviarFormulario}
          alteracao={{
            alterar: true,
            dados: {
              cpf: "99988877766",
              nome: "João Silva",
              email: "joaosilva@email.com",
              telefone: "79 9 9988-7766",
              endereco: "Rua das Flores, N° 123",
              horario_de_trabalho: "Seg-Sex,08h-18h",
              data_de_nascimento: "2000-03-08",
              tipo: "p",
              formacao: "Bacharelado em Matemática",
              escolaridade: null,
              habilidades: null,
              disciplinas: [{codigo: 'MAT101', nome: 'Matemática'}, {codigo: "FIS123", nome: "Física"}],
              cargos: [{"id": 1, "nome": "Professor", "salario": 3060.0, "data_contrato": "2021-12-31"}]
            },
            chave: "99988877766"
            }}
          />
        </BrowserRouter>
      )
    });
    
    it ("verifica se os dados foram carregados", async () => {

      // pegar os campos
      const nomeInput = screen.getByPlaceholderText(/Cristóvão Colombo/i);
      const emailInput = screen.getByLabelText(/Email:/i);
      const cpfInput = screen.getByLabelText(/CPF:/i);
      const dataDeNascimentoInput = screen.getByLabelText(/Data de Nascimento:/i);
      const telefoneInput = screen.getByLabelText(/Telefone:/i);
      const horarioDeTrabalhoInput = screen.getByLabelText(/Horário de Trabalho:/i);
      const tipoInput = screen.getByLabelText(/Tipo:/i);
      const enderecoInput = screen.getByLabelText(/Endereço:/i);
      const formacaoInput = screen.getByLabelText(/Formação:/i);
      const codigosDisciplinasInput = screen.getByLabelText(/Código\(s\) da\(s\) Disciplinas:/i);


      await waitFor(() => {
        // verificar se estão com os valores que recebe
        expect(nomeInput.value).toBe('João Silva');
        expect(emailInput.value).toBe('joaosilva@email.com');
        expect(cpfInput.value).toBe('999.888.777-66');
        expect(dataDeNascimentoInput.value).toBe('2000-03-08');
        expect(telefoneInput.value).toBe('79 9 9988-7766');
        expect(horarioDeTrabalhoInput.value).toBe('Seg-Sex,08h-18h');
        expect(tipoInput.value).toBe('p');
        expect(enderecoInput.value).toBe('Rua das Flores, N° 123');
        expect(formacaoInput.value).toBe('Bacharelado em Matemática');
        expect(codigosDisciplinasInput.value).toBe('MAT101,FIS123');
        expect(screen.getByRole("cell", { name: "Professor"})).toBeVisible();
        expect(screen.getByText("R$ 3.060,00")).toBeVisible();
        expect(screen.getByRole("cell", { name: "31-12-2021"})).toBeVisible();
      })

    });

  });

})