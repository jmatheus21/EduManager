import React, { useEffect } from "react";
import useApi from "../../hooks/useApi.jsx";
import { Container } from "react-bootstrap";
import { BarraDeBusca, Titulo, Listagem } from "../../components";

const colunas = [
    { field: "id", headerName: "#", flex: 1, align: "center", headerAlign: "center" },
    { field: "turma_id", headerName: "Turma", flex: 1, align: "center", headerAlign: "center" },
    { field: "disciplina_codigo", headerName: "Disciplina", flex: 1, align: "center", headerAlign: "center" },
    { field: "usuario_cpf", headerName: "Professor", flex: 1, align: "center", headerAlign: "center" },
    { field: "hora_inicio", headerName: "H.Início", flex: 1, align: "center", headerAlign: "center" },
    { field: "hora_fim", headerName: "H.Fim", flex: 1, align: "center", headerAlign: "center" },
    { field: "dias_da_semana", headerName: "Dias da Semana", flex: 1, align: "center", headerAlign: "center" }
];

/**
 * Componente para consultar aulas.
 * Este componente permite ao usuário buscar aulas pelo id e exibe uma lista de aulas cadastradas.
 *
 * @returns {JSX.Element} O componente de consulta de aulas.
 */
const ConsultarAula = () => {
    // Configuração padrão
    const api = useApi("/api");

    /**
     * Efeito para buscar as aulas ao carregar o componente.
     */
    useEffect(() => {
        api.fetchData("/aula");
    }, []);

    // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
    if (api.loading) return <p>Carregando...</p>;

    // Exibe mensagem de erro caso ocorra um erro na requisição
    if (api.error) return <p>Erro: {api.error}</p>;

    return (
        <Container fluid>
            <Titulo>Consultar Aulas</Titulo>
            <BarraDeBusca
                atributoNome={"Id da aula"}
                tipo={"number"}
                placeholder={"Exemplo: 1"}
                min={1}
                rota={"aula"}
                entidade={"aula"}
            />
            <Listagem colunas={colunas} data={api.data} pk={colunas[0].field} />
        </Container>
    );
};

export default ConsultarAula;