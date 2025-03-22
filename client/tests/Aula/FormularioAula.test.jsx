import React from "react";
import {
  render,
  screen,
  fireEvent,
  waitFor,
  act
} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { FormularioAula } from "../../src/pages/Aula";
import Formulario from "../../src/pages/Aula/components/Formulario";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/aula",
  }),
  useNavigate: jest.fn(),
}));

/**
 * Testes unitários para o componente FormularioAula.
 * Este conjunto de testes verifica a renderização correta do componente
 * e a exibição de mensagens de sucesso/erro.
 */
describe("FormularioAula Component", () => {
  describe("Cadastrar Aula", () => {
    beforeEach(() => {
      render(
        <BrowserRouter>
          <FormularioAula />
        </BrowserRouter>
      );
    });

    it("renderiza o formulário corretamente", () => {
      // Verifica se o título da página foi renderizado
      expect(screen.getByText(/Cadastrar Aula/i)).toBeVisible();

      // Verifica se o campo "Id da Turma:" foi renderizado
      expect(screen.getByLabelText(/Id da Turma:/i)).toBeVisible();

      // Verifica se o campo "Código da Disciplina:" foi renderizado
      expect(screen.getByLabelText(/Código da Disciplina:/i)).toBeVisible();

      // Verifica se o campo "CPF do Professor:" foi renderizado
      expect(screen.getByLabelText(/CPF do Professor:/i)).toBeVisible();

      // Verifica se o campo "Hora de Início:" foi renderizado
      expect(screen.getByLabelText(/Hora de Início:/i)).toBeVisible();

      // Verifica se o campo "Hora do Fim:" foi renderizado
      expect(screen.getByLabelText(/Hora do Fim:/i)).toBeVisible();

      // Verifica se o campo "Dias da Semana:" foi renderizado
      expect(screen.getByText(/Dias da Semana:/i)).toBeVisible();

      //Verifica se os dias da semana foram renderizados
      expect(screen.getByText(/Segunda/i)).toBeVisible();
      expect(screen.getByText(/Terça/i)).toBeVisible();
      expect(screen.getByText(/Quarta/i)).toBeVisible();
      expect(screen.getByText(/Quinta/i)).toBeVisible();
      expect(screen.getByText(/Sexta/i)).toBeVisible();
      expect(screen.getByText(/Sábado/i)).toBeVisible();

      // Verifica se o botão foi renderizado
      expect(screen.getByText(/Finalizar/i)).toBeVisible();
    });

    it("exibe mensagem de erro ao enviar formulário sem preencher campos obrigatórios", async () => {
      // Clica no botão de finalizar sem preencher os campos obrigatórios
      const botao = screen.getByText(/Finalizar/i);
      fireEvent.click(botao);

      // Verifica se as mensagens de erro foram exibidas, aguardando a renderização com await
      expect(
        await screen.findByText(/O id da turma é obrigatório/i)
      ).toBeVisible();
      expect(await screen.findByText(/O código da disciplina é obrigatório/i)).toBeVisible();
      expect(
        await screen.findByText(/O CPF do professor é obrigatório/i)
      ).toBeVisible();
      expect(await screen.findByText(/A hora de início é obrigatória/i)).toBeVisible();
      expect(
        await screen.findByText(/A hora do fim é obrigatória/i)
      ).toBeVisible();
      expect(
        await screen.findByText(/Os dias da semana são obrigatórios/i)
      ).toBeVisible();
    });

    // it("permite ao usuário digitar nos campos do formulário", async () => {
    //   const idTurmaInput = screen.getByLabelText(/Id da Turma:/i);
    //   const codigoDisciplinaInput = screen.getByLabelText(/Código da Disciplina:/i);
    //   const cpfProfessorInput = screen.getByLabelText(/CPF do Professor:/i);
    //   const horaDeInicioInput = screen.getByLabelText(/Hora de Início:/i);
    //   const horaDoFimInput = screen.getByLabelText(/Hora do Fim:/i);
    //   const diasDaSemanaInput = screen.getByLabelText(/Dias da Semana:/i);

    //   // realiza as ações
    //   await act(async () => {
    //     await userEvent.type(idTurmaInput, "1");
    //     await userEvent.type(codigoDisciplinaInput, "MAT001");
    //     await userEvent.selectOptions(cpfProfessorInput, "12345678910");
    //     await userEvent.selectOptions(horaDeInicioInput, "13:00:00");
    //     await userEvent.type(horaDoFimInput, "15:00:00");
    //     await userEvent.type(diasDaSemanaInput, "Quarta");
    //   });

    //   // verifica se os dados foram digitados corretamente
    //   expect(idTurmaInput.value).toBe("1");
    //   expect(codigoDisciplinaInput.value).toBe("MAT001");
    //   expect(cpfProfessorInput.value).toBe("12345678910");
    //   expect(horaDeInicioInput.value).toBe("13:00:00");
    //   expect(horaDoFimInput.value).toBe("15:00:00");
    //   expect(diasDaSemanaInput.value).toBe("Quarta");
    // });
  });

  // describe("Formulario da Aula", () => {
  //   const mockEnviarFormulario = jest.fn();

  //   beforeEach(() => {
  //     render(
  //       <BrowserRouter>
  //         <Formulario
  //           enviarFormulario={mockEnviarFormulario}
  //           alteracao={{
  //             alterar: false,
  //             dados: {},
  //             chave: undefined,
  //           }}
  //         />
  //       </BrowserRouter>
  //     );
  //   });

  //   it("verificar se o formulário está sendo enviado", async () => {

  //     const idTurmaInput = screen.getByLabelText(/Id da Turma:/i);
  //     const codigoDisciplinaInput = screen.getByLabelText(/Código da Disciplina:/i);
  //     const cpfProfessorInput = screen.getByLabelText(/CPF do Professor:/i);
  //     const horaDeInicioInput = screen.getByLabelText(/Hora de Início:/i);
  //     const horaDoFimInput = screen.getByLabelText(/Hora do Fim:/i);
  //     const diasDaSemanaInput = screen.getByLabelText(/Dias da Semana:/i);
  //     const botao = screen.getByText(/Finalizar/i);

  //     // realiza as ações
  //     await act(async () => {
  //       await userEvent.type(idTurmaInput, "1");
  //       await userEvent.type(codigoDisciplinaInput, "MAT001");
  //       await userEvent.selectOptions(cpfProfessorInput, "12345678910");
  //       await userEvent.selectOptions(horaDeInicioInput, "13:00:00");
  //       await userEvent.type(horaDoFimInput, "15:00:00");
  //       await userEvent.type(diasDaSemanaInput, "Quarta");
  //       await userEvent.click(botao);
  //     });

  //     await waitFor(() => {
  //       expect(mockEnviarFormulario).toHaveBeenCalledTimes(1);
  //       expect(mockEnviarFormulario).toHaveBeenCalledWith(
  //         {
  //           turma_id: 1,
  //           disciplina_codigo: "MAT001",
  //           usuario_cpf: "12345678910",
  //           hora_inicio: "M",
  //           hora_fim: "15:00:00",
  //           dias_da_semana: "Quarta",
  //         }
  //       );
  //     });
  //   });
  // });
});
