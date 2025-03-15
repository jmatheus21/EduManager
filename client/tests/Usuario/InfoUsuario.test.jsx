import React from "react";
import { render, screen, waitFor, act, logRoles } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { InfoUsuario } from "../../src/pages/Usuario";

// Mock do useLocation e useNavigate
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
    pathname: "/usuario/99988877766",
    search: ""
  }),
  useNavigate: jest.fn(),
  useParams: () => ({
    chave: "99988877766"
  }),
}));

jest.mock("../../src/hooks/useApi", () => ({
    __esModule: true,
    default: () => ({
        deleteData: jest.fn().mockResolvedValue({ success: true }),
        fetchData: jest.fn().mockResolvedValue({ success: true }),
        loading: false,
        error: null,
        data: {
          cpf: "99988877766" ,
          nome: "João Silva",
          email: "joaosilva@email.com",
          senha: "asmdbhdgfksgfldhoguoertknvb1344",
          telefone: "79 9 9988-7766",
          endereco: "Rua das Flores, N° 123",
          horario_de_trabalho: "Seg-Sex,08h-18h",
          data_de_nascimento: "2000-03-08",
          tipo: "p",
          formacao: "Bacharelado em Matemática",
          escolaridade: null,
          habilidades: null,
          disciplinas: [{codigo: 'MAT101', nome: 'Matemática'}, {codigo: "FIS123", nome: "Física"}, {codigo: "QUI123", nome: "Química"}],
          cargos: [{"id": 1, "nome": "Professor", "salario": 3060.0, "data_contrato": "2021-12-31"}, {"id": 2, "nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}]
        }
    })
}));


describe("InfoUsuario Component", () => {

    beforeEach(() => {
        render(
            <BrowserRouter>
                <InfoUsuario />
            </BrowserRouter>
        )
    })

    it ("renderiza todos os componentes na tela", () => { 
               
        // Verifica se o título da página foi renderizado
        expect(screen.getByText(/Informações do Usuário/i)).toBeVisible();

        // Verifica se o campo referente ao cpf foi renderizado
        expect(screen.getByText(/CPF:/i)).toBeVisible();

        // Verifica se o campo referente ao nome foi renderizado 
        expect(screen.getByRole("heading", { name: /Nome:/i })).toBeVisible();

        // Verifica se o campo referente ao telefone foi renderizado
        expect(screen.getByText(/Telefone:/i)).toBeVisible();

        // Verifica se o campo referente ao endereço foi renderizado
        expect(screen.getByText(/Endereço:/i)).toBeVisible();

        // Verifica se o campo referente ao horário de trabalho foi renderizado
        expect(screen.getByText(/Horário de trabalho:/i)).toBeVisible();

        // Verifica se o campo referente a data de nascimento foi renderizado
        expect(screen.getByText(/Data de nascimento:/i)).toBeVisible();

        // Verifica se o campo referente ao tipo foi renderizado
        expect(screen.getByText(/Tipo:/i)).toBeVisible();
        
        // Verifica se o campo referente à formação foi renderizado
        expect(screen.getByText(/Formação:/i)).toBeVisible();

        // Verifica se o campo referente aos cargos foi renderizado
        expect(screen.getByText(/Cargos:/i)).toBeVisible();

        expect(screen.getByRole("row", { name: "# Nome Salário mensal Data de contrato" })).toBeVisible();

        // Verifica se o campo referente às disciplinas foi renderizado
        expect(screen.getByText(/Disciplinas:/i)).toBeVisible();

        // Verifica se o botão 'Alterar' foi renderizado
        expect(screen.getByRole("button", { name: /Alterar/i })).toBeVisible();

        // Verifica se o botão 'Remover' foi renderizado
        expect(screen.getByRole("button", { name: /Remover/i })).toBeVisible();

    });
    

    it("renderiza todos os dados recebidos da API", async () => {

      await waitFor(() => {

        expect(screen.getByText("999.888.777-66")).toBeVisible();

        expect(screen.getByText("João Silva")).toBeVisible();

        expect(screen.getByText("joaosilva@email.com")).toBeVisible();

        expect(screen.getByText("79 9 9988-7766")).toBeVisible();

        expect(screen.getByText("Rua das Flores, N° 123")).toBeVisible();
        
        expect(screen.getByText("Seg-Sex,08h-18h")).toBeVisible();

        expect(screen.getByText("08-03-2000")).toBeVisible();

        expect(screen.getByTestId("usuario_tipo")).toBeVisible();

        expect(screen.getByText("Bacharelado em Matemática")).toBeVisible();
        
        expect(screen.getByText(/Matemática \(MAT101\)/)).toBeVisible();
        expect(screen.getByText(/Física \(FIS123\) e/)).toBeVisible();
        expect(screen.getByText(/Química \(QUI123\)/)).toBeVisible();

        // tabela cargos
        expect(screen.getByRole("gridcell", { name: "1" })).toBeVisible();
        expect(screen.getByRole("gridcell", { name: "Professor" })).toBeVisible();
        expect(screen.getByText("R$ 3.060,00")).toBeVisible();
        expect(screen.getByRole("gridcell", { name: "31-12-2021" })).toBeVisible();
        
        expect(screen.getByRole("gridcell", { name: "2" })).toBeVisible();
        expect(screen.getByRole("gridcell", { name: "Administrador de Recursos" })).toBeVisible();
        expect(screen.getByText("R$ 1.040,00")).toBeVisible();
        expect(screen.getByRole("gridcell", { name: "31-12-2027" })).toBeVisible();

        
      });
      
      
    });

    it("abre modal de remover elemento", async () => {
      
      const botaoRemover = screen.getByRole("button", { name: /Remover/i });
      
      await act ( async () => {
        await userEvent.click(botaoRemover);
      });
      
      const modalRemover = screen.getByText(/Remover Usuário/i);
      expect(modalRemover).toBeVisible();

    });

});