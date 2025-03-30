import { useState } from "react";
import useApi from "../../hooks/useApi";
import { Botao } from "../../components/Botao";
import {
  Alert,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { Container } from "react-bootstrap";
import { Titulo } from "../../components";
import { Form } from "react-bootstrap";

const GerarBoletim = () => {
  const [matricula, setMatricula] = useState("");
  const [show, setShow] = useState(false);
  const [error, setError] = useState("");
  const { data, downloadFile, fetchData } = useApi("/api");

  const buscarBoletim = async (e) => {
    e.preventDefault();

    if (!matricula) {
      alert("Por favor, insira uma matrícula");
      return;
    }

    try {
      const response = await fetchData(`/boletim/${matricula}?preview=true`);

      if (response) setShow(true);
    } catch (e) {
      setError(e.message);
      setShow(false);

      setTimeout(() => {
        setError("");
      }, 5000);
    }
  };

  const handleDownload = async () => {
    if (!matricula) {
      alert("Por favor, insira uma matrícula");
      return;
    }

    try {
      await downloadFile(`/boletim/${matricula}`, `boletim_${matricula}.pdf`);
    } catch (err) {
      alert("Erro no download");
    }
  };

  return (
    <Container fluid>
      <Titulo>Gerar Boletim</Titulo>
      <Container fluid>
        <Form onSubmit={buscarBoletim} className="d-flex gap-3 my-3">
          <Form.Group className="d-flex flex-fill align-items-center gap-3">
            <Form.Label style={{ whiteSpace: "nowrap" }}>
              Matrícula do aluno:{" "}
            </Form.Label>
            <Form.Control
              type="text"
              required
              className="p-2"
              value={matricula}
              onChange={(e) => setMatricula(e.target.value)}
              placeholder="Digite a matrícula"
            />
          </Form.Group>
          <Botao.Base title="buscar" type="submit" />
        </Form>
      </Container>
      {error && (
        <Alert severity="error" className="p-3 d-flex gap-2">
          {error}
        </Alert>
      )}
      {show ? (
        <>
          <TableContainer component={Paper} className="my-3">
            <Table
              sx={{ minWidth: "500px", maxHeight: "500px", overflowY: "auto" }}
              aria-label="simple table"
            >
              <TableHead>
                <TableRow>
                  <TableCell className="p-2 fw-bold fs-lg-5">
                    Disciplina
                  </TableCell>
                  <TableCell className="p-2 fw-bold fs-lg-5 text-center">
                    1° Unid.
                  </TableCell>
                  <TableCell className="p-2 fw-bold fs-lg-5 text-center">
                    2° Unid.
                  </TableCell>
                  <TableCell className="p-2 fw-bold fs-lg-5 text-center">
                    3° Unid.
                  </TableCell>
                  <TableCell className="p-2 fw-bold fs-lg-5 text-center">
                    4° Unid.
                  </TableCell>
                  <TableCell className="p-2 fw-bold fs-lg-5 text-center">
                    Ausências
                  </TableCell>
                  <TableCell className="p-2 fw-bold fs-lg-5 text-center">
                    Média Final
                  </TableCell>
                  <TableCell className="p-2 fw-bold fs-lg-5 text-center">
                    Situação
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data &&
                  data.boletim.map((item) => (
                    <TableRow key={item.disciplina}>
                      <TableCell className="p-2">{item.disciplina}</TableCell>
                      <TableCell className="p-2 text-center">
                        {item.u1}
                      </TableCell>
                      <TableCell className="p-2 text-center">
                        {item.u2}
                      </TableCell>
                      <TableCell className="p-2 text-center">
                        {item.u3}
                      </TableCell>
                      <TableCell className="p-2 text-center">
                        {item.u4}
                      </TableCell>
                      <TableCell className="p-2 text-center">
                        {item.media}
                      </TableCell>
                      <TableCell className="p-2 text-center">
                        {item.ausencias}
                      </TableCell>
                      <TableCell className="p-2 text-center">
                        {item.situacao}
                      </TableCell>
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </TableContainer>
          <Botao.Group>
            <Botao.Base
              title={"Download"}
              onClick={handleDownload}
              disabled={!data}
            />
          </Botao.Group>
        </>
      ) : (
        <p className="text-center mt-5">Insira a matrícula de um aluno</p>
      )}
    </Container>
  );
};

export default GerarBoletim;
