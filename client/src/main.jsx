import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import HomePage from "./pages/Home/HomePage.jsx";
import Gerenciar from "./pages/Gerenciar/Gerenciar.jsx";
import { ConsultarSala, FormularioSala, InfoSala } from "./pages/Sala";
import { ConsultarDisciplina, FormularioDisciplina } from "./pages/Disciplina";
import { ConsultarCalendario, FormularioCalendario, InfoCalendario } from "./pages/Calendario";
import { ConsultarUsuario, FormularioUsuario, InfoUsuario } from "./pages/Usuario";
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

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route index element={<HomePage />} />
        <Route path="sala" element={<Gerenciar menus={criarMenu("sala")} />}>
          <Route index element={<ConsultarSala />} />
          <Route path="cadastrar" element={<FormularioSala />} />
          <Route path=":chave" element={<InfoSala />} />
          <Route path="alterar/:chave" element={<FormularioSala />} />
        </Route>
        <Route path="disciplina" element={<Gerenciar menus={criarMenu("disciplina")} />}>
          <Route index element={<ConsultarDisciplina />} />
          <Route path="cadastrar" element={<FormularioDisciplina />} />
          {/* <Route path=":chave" element={<InfoDisciplina />} />
          <Route path="alterar/:chave" element={<FormularioDisciplina />} /> */}
        </Route>
        <Route path="calendario" element={<Gerenciar menus={criarMenu("calendario")} />}>
          <Route index element={<ConsultarCalendario />} />
          <Route path="cadastrar" element={<FormularioCalendario />} />
          <Route path=":chave" element={<InfoCalendario />} />
          <Route path="alterar/:chave" element={<FormularioCalendario />} />
        </Route>
        <Route path="usuario" element={<Gerenciar menus={criarMenu("usuario")} />}>
          <Route index element={<ConsultarUsuario />} />
          <Route path="cadastrar" element={<FormularioUsuario />} />
          <Route path=":chave" element={<InfoUsuario />} />
          <Route path="alterar/:chave" element={<FormularioUsuario />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
