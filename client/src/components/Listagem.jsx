import React from "react";
import { Container } from "react-bootstrap";
import { DataGrid } from "@mui/x-data-grid"

export const inverterData = (data) => {
  const [ano, mes, dia] = data.split('-');
  return `${dia}-${mes}-${ano}`;
};

export const formatarCpf = (cpf) => {
  cpf = cpf.replace(/\D/g, '');
  return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

/**
 * Componente para exibir a tabela de listagem dos objetos.
 * Este componente permite visualizar uma tabela com todos os objetos do tipo da entidade ou conforme configurado no backend.
 *
 * @returns {JSX.Element} O componente de listagem.
 */
const Listagem = ({ colunas, data, pk }) => {

  return (
    <Container fluid className="overflow-x-auto">
      <DataGrid 
        rows={data}
        columns={colunas}
        getRowId={(row) => row[pk]}
        initialState={{
          pagination: {
            paginationModel: {
              pageSize: 10,
            },
          },
        }}
        sx = {{
          overflowX: "auto",
          "@media (max-width: 768px)": {
            minWidth: "100%",
          },
        }}
        pageSizeOptions={[10]}
        disableRowSelectionOnClick
      />
    </Container>
  );
};

export default Listagem;
