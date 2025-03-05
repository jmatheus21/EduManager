import React from "react";
import { Table } from "react-bootstrap";

/**
 * Componente para exibir a tabela de listagem dos objetos.
 * Este componente permite visualizar uma tabela com todos os objetos do tipo da entidade ou conforme configurado no backend.
 *
 * @returns {JSX.Element} O componente de listagem.
 */
const Listagem = ({ colunas, data, pk }) => {
  return (
    <Table striped bordered hover>
      <thead>
        <tr className="text-center">
          {colunas.map((coluna) => (
            <th key={coluna.campo} className="p-2">
              {coluna.label}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data?.sort((a, b) => a[pk] - b[pk]).map((dados, index) => (
          <tr key={index}>
            {colunas.map((coluna) => (
              <td key={coluna.campo} className="p-2">
                {dados[coluna.campo]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default Listagem;
