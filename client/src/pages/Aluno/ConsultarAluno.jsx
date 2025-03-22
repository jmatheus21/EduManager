import React, { useEffect } from "react";
import useApi from "../../hooks/useApi.jsx";
import { Container } from "react-bootstrap";
import { inverterData } from "../../components/Listagem.jsx"; 
import { BarraDeBusca, Titulo, Listagem } from "../../components";

const colunas = [
    { field: "matricula", headerName: "Matrícula", flex: 1, align: "center", headerAlign: "center" },
    { field: "nome", headerName: "Nome", flex: 1, align: "center", headerAlign: "center" },
    { field: "turma_id", headerName: "Turma", flex: 1, align: "center", headerAlign: "center" },
    { field: "email", headerName: "E-mail", flex: 1, align: "center", headerAlign: "center" },
    { field: "telefone", headerName: "Telefone", flex: 1, align: "center", headerAlign: "center"},
    { field: "data_de_nascimento", headerName: "Data de Nascimento", flex: 1, align: "center", headerAlign: "center", valueGetter: (value, _row) => inverterData(value) },
];

/**
 * Componente para consultar alunos.
 * Este componente permite ao usuário buscar alunos pela matricula e exibe uma lista de alunos cadastrados.
 *
 * @returns {JSX.Element} O componente de consulta de usuários.
 */
const ConsultarAluno = () => {
    // Configuração padrão
    const api = useApi("/api");
  
    /**
     * Efeito para buscar os usuários ao carregar o componente.
     */
    useEffect(() => {
      api.fetchData("/aluno");
    }, []);

    // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
    if (api.loading) return <p>Carregando...</p>;

    // Exibe mensagem de erro caso ocorra um erro na requisição
    if (api.error) return <p>Erro: {api.error}</p>;

    return (
        <Container fluid>
            <Titulo>Consultar Alunos</Titulo>
            <BarraDeBusca
                atributoNome={"Matrícula"}
                tipo={"text"}
                placeholder={"Exemplo: 202600000001"}
                minLength={12}
                maxLength={12}
                rota={"aluno"}
                entidade={"aluno"}
            />
            <Listagem colunas={colunas} data={api.data} pk={colunas[0].field} />
        </Container>
      );
    };
    
export default ConsultarAluno;