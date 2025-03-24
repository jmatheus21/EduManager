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
import { ConsultarAluno, FormularioAluno } from "./pages/Aluno";
import Matricula from "./pages/Matricula/Matricula.jsx"
import "./index.css";

const criarMenu = (entidade) => {
  return [
    {
      nome: "Consultar",
      url: `/${entidade}`,
    },
    {
      nome: "Cadastrar",
      url: `/${entidade}/cadastrar`,
    },
  ];
};

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
          <Route path="sala" element={<GerenciarProtegido menus={criarMenu("sala")} />}>
            <Route index element={<ConsultarSala />} />
            <Route path="cadastrar" element={<FormularioSala />} />
            <Route path=":chave" element={<InfoSala />} />
            <Route path="alterar/:chave" element={<FormularioSala />} />
          </Route>
          <Route path="disciplina" element={<GerenciarProtegido menus={criarMenu("disciplina")} />}>
            <Route index element={<ConsultarDisciplina />} />
            <Route path="cadastrar" element={<FormularioDisciplina />} />
            <Route path=":chave" element={<InfoDisciplina />} />
            <Route path="alterar/:chave" element={<FormularioDisciplina />} />
          </Route>
          <Route path="calendario" element={<GerenciarProtegido menus={criarMenu("calendario")} />}>
            <Route index element={<ConsultarCalendario />} />
            <Route path="cadastrar" element={<FormularioCalendario />} />
            <Route path=":chave" element={<InfoCalendario />} />
            <Route path="alterar/:chave" element={<FormularioCalendario />} />
          </Route>
          <Route path="usuario" element={<GerenciarProtegido menus={criarMenu("usuario")} />}>
            <Route index element={<ConsultarUsuario />} />
            <Route path="cadastrar" element={<FormularioUsuario />} />
            <Route path=":chave" element={<InfoUsuario />} />
            <Route path="alterar/:chave" element={<FormularioUsuario />} />
          </Route>
          <Route path="turma" element={<GerenciarProtegido menus={criarMenu("turma")} />}>
            <Route index element={<ConsultarTurma />} />
            <Route path="cadastrar" element={<FormularioTurma />} />
            <Route path=":chave" element={<InfoTurma />} />
            <Route path="alterar/:chave" element={<FormularioTurma />}/>
          </Route>
          <Route path="aluno" element={<GerenciarProtegido menus={criarMenu("aluno")} />}>
            <Route index element={<ConsultarAluno />} />
            <Route path="cadastrar" element={<FormularioAluno />} />
            {/* <Route path=":chave" element={<InfoAluno />} />
            <Route path="alterar/:chave" element={<FormularioAluno />}/> */}
          </Route>
          <Route path="matricula" element={<GerenciarProtegido menus={criarMenu("matricula")} />}>
            <Route index element={<Matricula />} />
            <Route path="cadastrar" element={<FormularioAluno />} />
            {/* <Route path=":chave" element={<InfoAluno />} />
            <Route path="alterar/:chave" element={<FormularioAluno />}/> */}
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);
