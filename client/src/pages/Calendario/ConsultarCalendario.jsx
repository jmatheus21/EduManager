import React, { useEffect } from "react";
import useApi from "../../hooks/useApi.jsx";
import { Container } from "react-bootstrap";
import { BarraDeBusca, Titulo, Listagem, Alerta } from "../../components";
import { inverterData } from "../../components/Listagem.jsx";

const anoAtual = new Date().getFullYear();

const colunas = [
  { field: "ano_letivo", headerName: "Ano letivo", flex: 1, align: "center", headerAlign: "center"},
  { field: "data_inicio", headerName: "Data de início", flex: 1, align: "center", headerAlign: "center", valueGetter: (value, _row) => inverterData(value)},
  { field: "data_fim", headerName: "Data de fim", flex: 1, align: "center", headerAlign: "center", valueGetter: (value, _row) => inverterData(value)},
  { field: "dias_letivos", headerName: "Dias letivos", flex: 1, align: "center", headerAlign: "center"},
];

/**
 * Componente para consultar calendários.
 * Este componente permite ao usuário buscar calendários por ano letivo e exibe uma lista de calendários cadastrados.
 *
 * @returns {JSX.Element} O componente de consulta de calendarios.
 */
const ConsultarCalendario = () => {
  // Configuração padrão
  const api = useApi("/api");

  /**
   * Efeito para buscar os calendários ao carregar o componente.
   */
  useEffect(() => {
    api.fetchData("/calendario");
  }, []);

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (api.loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  if (api.error) return <p>Erro: {api.error}</p>;

  return (
    <Container fluid>
      <Titulo>Consultar Calendários</Titulo>
      <BarraDeBusca
        atributoNome={"Ano letivo"}
        tipo={"number"}
        placeholder={`Exemplo: ${anoAtual}`}
        min={anoAtual}
        entidade={"calendario"}
      />
      <Alerta type={true} entidade={"calendário"} />
      <Listagem colunas={colunas} data={api.data} pk={colunas[0].field} />
    </Container>
  );
};

export default ConsultarCalendario;
