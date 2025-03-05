import React from "react";
import { Alert, Container } from "react-bootstrap";

const Alerta = ({ type }) => {
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
            ? "Sala removida com sucesso!"
            : "Sala cadastrada com sucesso!"}
        </Alert>
      )}
    </Container>
  );
};

export default Alerta;
