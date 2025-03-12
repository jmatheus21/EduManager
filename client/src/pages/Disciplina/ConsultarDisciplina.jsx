import React, { useEffect } from "react";
import useApi from "../../hooks/useApi.jsx";
import { Container } from "react-bootstrap";
import { BarraDeBusca, Titulo, Listagem, Alerta } from "../../components";

const colunas = [
    { field: "nome", headerName: "Nome", flex: 1, align: "center", headerAlign: "center" },
    { field: "codigo", headerName: "Código", flex: 1, align: "center", headerAlign: "center" },
    { field: "carga_horaria", headerName: "Carga Horária", flex: 1, align: "center", headerAlign: "center", valueGetter: (value) => `${value}h` }
];

/**
 * Componente para consultar disciplinas.
 * Este componente permite ao usuário buscar disciplinas pelo código e exibe uma lista de disciplinas cadastradas.
 *
 * @returns {JSX.Element} O componente de consulta de disciplinas.
 */
const ConsultarDisciplina = () => {
    // Configuração padrão
    const api = useApi("/api");

    /**
     * Efeito para buscar as disciplinas ao carregar o componente.
     */
    useEffect(() => {
        api.fetchData("/disciplina");
    }, []);

    // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
    if (api.loading) return <p>Carregando...</p>;

    // Exibe mensagem de erro caso ocorra um erro na requisição
    if (api.error) return <p>Erro: {api.error}</p>;

    return (
        <Container fluid>
            <Titulo>Consultar Disciplinas</Titulo>
            <BarraDeBusca
                atributoNome={"Código"}
                tipo={"text"}
                placeholder={"Exemplo: MAT001"}
                minLength={6}
                maxLength={10}
                entidade={"disciplina"}
            />
            <Alerta type={true} entidade={"Disciplina"} />
            <Listagem colunas={colunas} data={api.data} pk={colunas[0].field} />
        </Container>
    );
};

export default ConsultarDisciplina;
