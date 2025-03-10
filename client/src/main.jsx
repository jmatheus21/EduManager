import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import "bootstrap/dist/css/bootstrap.min.css";
import HomePage from "./pages/Home/HomePage.jsx";
import Gerenciar from "./pages/Gerenciar/Gerenciar.jsx";
import { ConsultarSala, FormularioSala, InfoSala } from "./pages/Sala";
import { ConsultarDisciplina, FormularioDisciplina } from "./pages/Disciplina";
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
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
