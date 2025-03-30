import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import ProtectedRoute from "./providers/ProtectedRoute.jsx";
import AuthProvider from "./providers/AuthProvider.jsx"
import HomePage from "./pages/Home/HomePage.jsx";
import Gerenciar from "./pages/Gerenciar/Gerenciar.jsx";
import Login from "./pages/Login/Login.jsx";
import { ConsultarSala, FormularioSala, InfoSala } from "./pages/Sala";
import { ConsultarDisciplina, FormularioDisciplina, InfoDisciplina } from "./pages/Disciplina";
import { ConsultarCalendario, FormularioCalendario, InfoCalendario } from "./pages/Calendario";
import { ConsultarUsuario, FormularioUsuario, InfoUsuario } from "./pages/Usuario";
import { ConsultarTurma, FormularioTurma, InfoTurma } from "./pages/Turma";
import { ConsultarAluno, FormularioAluno, InfoAluno } from "./pages/Aluno";
import { ConsultarAula, FormularioAula, InfoAula } from "./pages/Aula";
import { AlterarNotas, CadastrarNotas } from "./pages/Notas";
import { AlterarAusencias, RegistroAusencias } from "./pages/Ausencias";
import Matricula from "./pages/Matricula/Matricula.jsx"
import GerarBoletim from "./pages/Boletim/GerarBoletim.jsx";
import GerarHistorico from "./pages/Boletim/GerarHistorico.jsx";
import { criarMenuPadrao, criarMenuCustom, criarMenuSimples, criarMenuMatricular } from "./utils/mainUtils.jsx";
import "./index.css";

const withProtectedRoute = (Component) => {
  return (props) => (
    <ProtectedRoute>
      <Component {...props} />
    </ProtectedRoute>
  );
};

const GerenciarProtegido = withProtectedRoute(Gerenciar)
const HomePageProtegida = withProtectedRoute(HomePage)

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
    <AuthProvider>
        <Routes>
          <Route path="login" element={<Login />} />
          <Route index element={<HomePageProtegida />} />
          <Route path="sala" element={<GerenciarProtegido menus={criarMenuPadrao("sala")} />}>
            <Route index element={<ConsultarSala />} />
            <Route path="cadastrar" element={<FormularioSala />} />
            <Route path=":chave" element={<InfoSala />} />
            <Route path="alterar/:chave" element={<FormularioSala />} />
          </Route>
          <Route path="disciplina" element={<GerenciarProtegido menus={criarMenuPadrao("disciplina")} />}>
            <Route index element={<ConsultarDisciplina />} />
            <Route path="cadastrar" element={<FormularioDisciplina />} />
            <Route path=":chave" element={<InfoDisciplina />} />
            <Route path="alterar/:chave" element={<FormularioDisciplina />} />
          </Route>
          <Route path="calendario" element={<GerenciarProtegido menus={criarMenuPadrao("calendario")} />}>
            <Route index element={<ConsultarCalendario />} />
            <Route path="cadastrar" element={<FormularioCalendario />} />
            <Route path=":chave" element={<InfoCalendario />} />
            <Route path="alterar/:chave" element={<FormularioCalendario />} />
          </Route>
          <Route path="usuario" element={<GerenciarProtegido menus={criarMenuPadrao("usuario")} />}>
            <Route index element={<ConsultarUsuario />} />
            <Route path="cadastrar" element={<FormularioUsuario />} />
            <Route path=":chave" element={<InfoUsuario />} />
            <Route path="alterar/:chave" element={<FormularioUsuario />} />
          </Route>
          <Route path="turma" element={<GerenciarProtegido menus={criarMenuPadrao("turma")} />}>
            <Route index element={<ConsultarTurma />} />
            <Route path="cadastrar" element={<FormularioTurma />} />
            <Route path=":chave" element={<InfoTurma />} />
            <Route path="alterar/:chave" element={<FormularioTurma />}/>
          </Route>
          <Route path="aluno" element={<GerenciarProtegido menus={criarMenuPadrao("aluno")} />}>
            <Route index element={<ConsultarAluno />} />
            <Route path="cadastrar" element={<FormularioAluno />} />
            <Route path=":chave" element={<InfoAluno />} />
            <Route path="alterar/:chave" element={<FormularioAluno />} />
          </Route>
          <Route path="aula" element={<GerenciarProtegido menus={criarMenuPadrao("aula")} />}>
            <Route index element={<ConsultarAula />} />
            <Route path="cadastrar" element={<FormularioAula />} />
            <Route path=":chave" element={<InfoAula />} />
            <Route path="alterar/:chave" element={<FormularioAula />}/>
          </Route>
          <Route path="matricula" element={<GerenciarProtegido menus={criarMenuMatricular("matricula")} />}>
            <Route index element={<Matricula />} />
          </Route>
          <Route path="nota" element={<GerenciarProtegido menus={criarMenuCustom("nota")} />}>
              <Route index element={<CadastrarNotas />} />
              <Route path="alterar" element={<AlterarNotas />} />
          </Route>
          <Route path="ausencias" element={<GerenciarProtegido menus={criarMenuCustom("ausencias")} />}>
              <Route index element={<RegistroAusencias />} />
              <Route path="alterar" element={<AlterarAusencias />} />
          </Route>
          <Route path="boletim" element={<GerenciarProtegido menus={criarMenuSimples("boletim")}/>}>
              <Route index element={<GerarBoletim />} />
          </Route>
          <Route path="historico" element={<GerenciarProtegido menus={criarMenuSimples("historico")}/>}>
              <Route index element={<GerarHistorico />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);
