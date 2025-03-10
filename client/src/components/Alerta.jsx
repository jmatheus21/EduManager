import React from "react";
import { Alert, Container } from "react-bootstrap";
import { useLocation } from 'react-router'

const Alerta = ({ type, entidade }) => {
  const url = useLocation();
  const queryParams = new URLSearchParams(url.search);
  const successParam = queryParams.get("success");
  let typeParam;
  if (type) typeParam = queryParams.get("type");

  return (
    <Container fluid>
      {successParam && (
        <Alert variant="success" className="p-3 mb-3">
          {!type || typeParam == "remocao"
            ? `${entidade} removid${entidade.endsWith("a") ? "a" : "o"} com sucesso!`
            : `${entidade} cadastrad${entidade.endsWith("a") ? "a" : "o"} com sucesso!`}
        </Alert>
      )}
    </Container>
  );
};

export default Alerta;
