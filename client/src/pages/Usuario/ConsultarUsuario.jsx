import React, { useEffect } from "react";
import useApi from "../../hooks/useApi.jsx";
import { Container } from "react-bootstrap";
import { BarraDeBusca, Titulo, Listagem } from "../../components";
import { inverterData, formatarCpf } from "../../components/Listagem.jsx"; 

const colunas = [
    { field: "cpf", headerName: "CPF", flex: 1, align: "center", headerAlign: "center", valueGetter: (value, _row) => formatarCpf(value) },
    { field: "nome", headerName: "Nome", flex: 1, align: "center", headerAlign: "center" },
    { field: "tipo", headerName: "Tipo", flex: 1, align: "center", headerAlign: "center", valueGetter: (value, _row) => value == "p"? "Professor" : "Funcionário" },
    { field: "email", headerName: "E-mail", flex: 1, align: "center", headerAlign: "center" },
    { field: "telefone", headerName: "Telefone", flex: 1, align: "center", headerAlign: "center"},
    { field: "data_de_nascimento", headerName: "Data de Nascimento", flex: 1, align: "center", headerAlign: "center", valueGetter: (value, _row) => inverterData(value) },
];

/**
 * Componente para consultar usuários.
 * Este componente permite ao usuário buscar usuários pelo cpf e exibe uma lista de usuários cadastrados.
 *
 * @returns {JSX.Element} O componente de consulta de usuários.
 */
const ConsultarUsuario = () => {
    // Configuração padrão
    const api = useApi("/api");
  
    /**
     * Efeito para buscar os usuários ao carregar o componente.
     */
    useEffect(() => {
      const response = api.fetchData("/usuario");
    }, []);

    // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
    if (api.loading) return <p>Carregando...</p>;

    // Exibe mensagem de erro caso ocorra um erro na requisição
    if (api.error) return <p>Erro: {api.error}</p>;

    return (
        <Container fluid>
          <Titulo>Consultar Usuários</Titulo>
          <BarraDeBusca
            atributoNome={"CPF"}
            tipo={"text"}
            placeholder={"Exemplo: 99988877765"}
            minLength={5}
            maxLength={20}
            entidade={"usuario"}
          />
          <Listagem colunas={colunas} data={api.data} pk={colunas[0].field} />
        </Container>
      );
    };
    
export default ConsultarUsuario;