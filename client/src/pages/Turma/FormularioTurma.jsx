import React, { useEffect, useState } from "react";
import { Col, Container, Form, Row, Alert } from "react-bootstrap";
import useApi from "../../hooks/useApi";
import { useNavigate, useParams } from "react-router-dom";
import { Titulo, BotaoCadastrar, BotaoAlterar } from "../../components";
import { useForm } from "react-hook-form";

/**
 * Componente para cadastrar ou alterar uma disciplina.
 * Este componente permite ao usuário cadastrar uma nova disciplina ou alterar os dados de uma disciplina existente.
 * 
 * @returns {JSX.Element} O componente de formulário para cadastrar ou alterar uma disciplina.
 */
const FormularioTurma = () => {
    // const { register, handleSubmit, setError, formState: { errors } } = useForm(); // esse é o novo formulário

    // // Configuração padrão
    // const [titulo, setTitulo] = useState("Cadastrar");
    // const api = useApi("/api");
    // const navigate = useNavigate();
    // // const url = useLocation();
    // const { chave } = useParams();

    // /**
    //  * Efeito para carregar os dados da disciplina quando o componente é montado ou quando o caminho da URL ou o parâmetro `chave` mudam.
    //  * Se o caminho da URL incluir "alterar", o título do formulário será alterado para "Alterar" e os dados da disciplina serão carregados.
    //  */
    // // useEffect(() => {
    //     // const carregarDados = async () => {
    //     //     if (url.pathname.includes("alterar")) {
    //     //         setTitulo("Alterar");

    //     //         try {
    //     //             const response = await api.fetchData(`/disciplina/${chave}`);
    //     //             if (response) {
    //     //                 setCodigo(response.codigo);
    //     //                 setCapacidade(response.capacidade);
    //     //                 setLocalizacao(response.localizacao);
    //     //             }
    //     //         } catch (error) {
    //     //             setTextAlert(error);
    //     //             console.error("Erro ao carregar dados da disciplina:", error);
    //     //         }
    //     //     }
    //     // };

    //     // carregarDados();
    // // }, [url.pathname, chave]);

    // /**
    //  * Função para lidar com o envio do formulário.
    //  * Dependendo do caminho da URL, a função irá cadastrar uma nova disciplina ou alterar uma disciplina existente.
    //  * 
    //  * @param {Event} event - O evento de submissão do formulário.
    //  */
    // const enviarFormulario = async (data) => {
    //     try {
    //         if (location.pathname.includes("alterar")) {
    //             await api.updateData(`/disciplina/${chave}`, data);

    //             navigate(`/disciplina/${chave}?success=true`);
    //         } else {
    //             await api.createData("/disciplina", data);

    //             navigate("/disciplina?success=true&type=cadastro");
    //         }
    //     } catch (error) {
    //         console.error(error);

    //         if (error.message == "Disciplina já existe") {
    //             setError("codigo", { type: "equal" });
    //         }
    //     }
    // };

    // /**
    //  * Função para, na alteração, voltar a página de informações
    //  */
    // const funcaoVoltar = () => navigate(`/disciplina/${chave}`);

    // // Exibe mensagem de carregamento enquanto os dados estão sendo buscados
    // if (titulo.includes("Alterar") && api.loading) return <p>Carregando...</p>;

    // // Exibe mensagem de erro caso ocorra um erro na requisição
    // if (titulo.includes("Alterar") && api.error) return <p>Erro: {api.error}</p>;

    // return (
    //     <Container fluid className="d-flex flex-column">
    //         <Titulo>{titulo} Disciplina</Titulo>
    //         <Form className="flex-fill d-flex flex-column justify-content-between mt-4" onSubmit={handleSubmit(enviarFormulario)}>
    //             <Container fluid className="d-grid gap-3">
    //                 <Row className="gap-5">
    //                     <Col>
    //                         <Form.Group className="d-flex flex-column gap-1">
    //                             <Form.Label htmlFor="nome">Nome: <span className="text-danger">*</span></Form.Label>
    //                             <Form.Control
    //                                 id="nome"
    //                                 type="text"
    //                                 className="p-2"
    //                                 {...register("nome", { required: true, minLength: 3, maxLength: 50 })}
    //                             />
    //                         </Form.Group>
    //                         <Alert variant="white" className={`${errors.nome ? "" : "d-none"} text-danger`}>
    //                             {errors?.nome?.type == "required" && "O nome da disciplina é obrigatório"}
    //                             {errors?.nome?.type == "minLength" && "O nome da disciplina deve ter no mínimo 3 caracteres"}
    //                             {errors?.nome?.type == "maxLength" && "O nome da disciplina deve ter no máximo 50 caracteres"}
    //                         </Alert>
    //                     </Col>
    //                 </Row>
    //                 <Row className="gap-5">
    //                     <Col>
    //                         <Form.Group className="d-flex flex-column gap-1">
    //                             <Form.Label htmlFor="codigo">Código: <span className="text-danger">*</span></Form.Label>
    //                             <Form.Control
    //                                 id="codigo"
    //                                 type="text"
    //                                 className="p-2"
    //                                 {...register("codigo", { required: true, minLength: 6, maxLength: 10, pattern: /^[A-Z]{3}\d{3}$/ })}
    //                             />
    //                         </Form.Group>
    //                         <Alert variant="white" className={`${errors.codigo ? "" : "d-none"} text-danger`}>
    //                             {errors?.codigo?.type == "equal" && "O código da disciplina já existe"}
    //                             {errors?.codigo?.type == "required" && "O código da disciplina é obrigatório"}
    //                             {errors?.codigo?.type == "minLength" && "O código da disciplina deve ter no mínimo 6 caracteres"}
    //                             {errors?.codigo?.type == "maxLength" && "O código da disciplina deve ter no máximo 10 caracteres"}
    //                             {errors?.codigo?.type == "pattern" && "O código da disciplina não está no formato correto. Utilize três letras maiúsculas seguidas de três números (ex: MAT123)"}
    //                         </Alert>
    //                     </Col>
    //                     <Col>
    //                         <Form.Group className="d-flex flex-column gap-1">
    //                             <Form.Label htmlFor="carga_horaria">Carga Horária: <span className="text-danger">*</span></Form.Label>
    //                             <Form.Control
    //                                 id="carga_horaria"
    //                                 type="number"
    //                                 className="p-2"
    //                                 {...register("carga_horaria", { required: true, min: 15, max: 120, valueAsNumber: true })}
    //                             />
    //                         </Form.Group>
    //                         <Alert variant="white" className={`${errors.carga_horaria ? "" : "d-none"} text-danger`}>
    //                             {errors?.carga_horaria?.type == "required" && "A carga horária é obrigatória"}
    //                             {errors?.carga_horaria?.type == "min" && "A carga horária deve ser de no mínimo 15"}
    //                             {errors?.carga_horaria?.type == "max" && "A carga horária deve ser no máximo 120"}
    //                         </Alert>
    //                     </Col>
    //                 </Row>
    //                 <Row className="gap-5">
    //                     <Col>
    //                         <Form.Group className="d-flex flex-column gap-1">
    //                             <Form.Label htmlFor="ementa">Ementa: </Form.Label>
    //                             <Form.Control
    //                                 id="ementa"
    //                                 type="text"
    //                                 className="p-2"
    //                                 {...register("ementa", { required: false, maxLength: 255 })}
    //                             />
    //                         </Form.Group>
    //                         <Alert variant="white" className={`${errors.ementa ? "" : "d-none"} text-danger`}>
    //                             {errors?.ementa?.type == "maxLength" && "A ementa deve ter no máximo 255 caracteres"}
    //                         </Alert>
    //                     </Col>
    //                 </Row>
    //                 <Row className="gap-5">
    //                     <Col>
    //                         <Form.Group className="d-flex flex-column gap-1">
    //                             <Form.Label htmlFor="bibliografia">Bibliografia: </Form.Label>
    //                             <Form.Control
    //                                 id="bibliografia"
    //                                 type="text"
    //                                 className="p-2"
    //                                 {...register("bibliografia", { required: false, maxLength: 255 })}
    //                             />
    //                         </Form.Group>
    //                         <Alert variant="white" className={`${errors.bibliografia ? "" : "d-none"} text-danger`}>
    //                             {errors?.bibliografia?.type == "maxLength" && "A bibliografia deve ter no máximo 255 caracteres"}
    //                         </Alert>
    //                     </Col>
    //                 </Row>
    //             </Container>
    //             {
    //                 titulo.includes("Alterar") ? <BotaoAlterar funcaoVoltar={funcaoVoltar} /> : <BotaoCadastrar />
    //             }
    //         </Form >
    //     </Container >
    // );
};

export default FormularioTurma;