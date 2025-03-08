import React, { useEffect } from "react";
import useApi from "../../hooks/useApi.jsx";
import { Container } from "react-bootstrap";
import { BarraDeBusca, Titulo, Listagem, Alerta } from "../../components";

const colunas = [
  { campo: "numero", label: "Número" },
  { campo: "capacidade", label: "Capacidade" },
  { campo: "localizacao", label: "Localização" },
];

/**
 * Componente para consultar salas.
 * Este componente permite ao usuário buscar salas por número e exibe uma lista de salas cadastradas.
 *
 * @returns {JSX.Element} O componente de consulta de salas.
 */
const ConsultarSala = () => {
  // Configuração padrão
  const api = useApi("/api");

  /**
   * Efeito para buscar as salas ao carregar o componente.
   */
  useEffect(() => {
    api.fetchData("/sala");
  }, []);

  // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
  if (api.loading) return <p>Carregando...</p>;

  // Exibe mensagem de erro caso ocorra um erro na requisição
  if (api.error) return <p>Erro: {api.error}</p>;

  return (
    <Container fluid>
      <Titulo>Consultar Salas</Titulo>
      <BarraDeBusca
        atributoNome={"Número"}
        tipo={"number"}
        placeholder={"Exemplo: 10"}
        min={1}
        max={100}
        entidade={"sala"}
      />
      <Alerta type={true} />
      <Listagem colunas={colunas} data={api.data} pk={colunas[0].campo} />
    </Container>
  );
};

export default ConsultarSala;
