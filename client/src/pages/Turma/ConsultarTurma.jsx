import React, { useEffect } from "react";
import useApi from "../../hooks/useApi.jsx";
import { Container } from "react-bootstrap";
import { BarraDeBusca, Titulo, Listagem, Alerta } from "../../components";

const colunas = [
    { field: "id", headerName: "#", flex: 1, align: "center", headerAlign: "center" },
    { field: "calendario_ano_letivo", headerName: "Ano Letivo", flex: 1, align: "center", headerAlign: "center" },
    { field: "ano", headerName: "Ano", flex: 1, align: "center", headerAlign: "center" },
    { field: "serie", headerName: "Série", flex: 1, align: "center", headerAlign: "center" },
    { field: "nivel_de_ensino", headerName: "Nível de Ensino", flex: 1, align: "center", headerAlign: "center" },
    { field: "turno", headerName: "Turno", flex: 1, align: "center", headerAlign: "center", valueGetter: (value, _row) => value == "M"? "Matutino" : value == "V" ? "Vespertino" : "Noturno" },
    { field: "status", headerName: "Status", flex: 1, align: "center", headerAlign: "center", valueGetter: (value, _row) => value == "A"? "Ativa" : "Consolidada" }
];

/**
 * Componente para consultar turmas.
 * Este componente permite ao usuário buscar turmas pelo id e exibe uma lista de turmas cadastradas.
 *
 * @returns {JSX.Element} O componente de consulta de turmas.
 */
const ConsultarTurma = () => {
    // Configuração padrão
    const api = useApi("/api");

    /**
     * Efeito para buscar as turmas ao carregar o componente.
     */
    useEffect(() => {
        api.fetchData("/turma");
    }, []);

    // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
    if (api.loading) return <p>Carregando...</p>;

    // Exibe mensagem de erro caso ocorra um erro na requisição
    if (api.error) return <p>Erro: {api.error}</p>;

    return (
        <Container fluid>
            <Titulo>Consultar Turmas</Titulo>
            <BarraDeBusca
                atributoNome={"Id da turma"}
                tipo={"number"}
                placeholder={"Exemplo: 1"}
                min={1}
                entidade={"turma"}
            />
            <Alerta type={true} entidade={"Turma"} />
            <Listagem colunas={colunas} data={api.data} pk={colunas[0].field} />
        </Container>
    );
};

export default ConsultarTurma;