import React, { useEffect, useState } from "react";
import { Button, Card, Form, Alert, Spinner } from "react-bootstrap";
import { useForm } from "react-hook-form";
import { useAuth } from "../../../contexts/AuthContext"
import isEmail from "validator/lib/isEmail";
import axios from "axios";

export default function LoginForm() {
  const { register, handleSubmit, setError, formState: { errors } } = useForm();
  const [loading, setLoading] = useState(false);
  const [loadingAuth, setLoadingAuth] = useState(true);
  const { validateToken } = useAuth();

  useEffect(() => {
    const verificarUsuario = async () => {
      try {
        await axios.get("api/auth/validate")
        window.location.href = "/";
      } catch (erro) {
        setLoadingAuth(false)
      }
    }

    verificarUsuario()
  }, [])

  const onSubmit = async (data) => {

    setLoading(true);

    try {
        await axios.post("api/auth/login", data, {
            withCredentials: true,
            headers: { "Content-Type": "application/json" }
        })

        await validateToken();

        window.location.href = "/";
    } catch (erro) {
        setError("root.serverError", { message: "Credenciais inválidas" })
    } finally {
        setLoading(false)
    }
  };

  if (loadingAuth) return <p>Verificando credenciais...</p>

  return (
    <div className="d-flex justify-content-center align-items-center min-vh-70">
      <Card className="w-100 p-5" style={{ maxWidth: "500px" }}>
        <Card.Body>
          <Card.Title className="text-center mb-4 fs-3 fw-bold">
            Login
          </Card.Title>
          <Card.Text className="text-muted text-center mb-4">
            Entre com suas credenciais para acessar sua conta
          </Card.Text>

          <Form onSubmit={handleSubmit(onSubmit)}>
            <Form.Group className="mb-3">
              <Form.Label htmlFor="email">E-mail</Form.Label>
              <Form.Control
                id="email"
                type="email"
                className="p-2 mt-2"
                placeholder="Digite seu e-mail"
                {...register("email", { required: true, minLength: 3, maxLength: 100, validate: (value) => isEmail(value) })}
              />
            <Alert variant="white" className={`${errors?.email? "" : "d-none"} text-danger`}>
                {!errors.root?.serverError && errors?.email?.type == "required" &&  "E-mail é obrigatório"}
                {!errors.root?.serverError && errors?.email?.type == "minLength" && "E-mail precisa ter no mínimo 3 caracteres"}
                {!errors.root?.serverError && errors?.email?.type == "maxLength" && "E-mail precisa ter no máximo 100 caracteres"}
                {!errors.root?.serverError && errors?.email?.type == "validate" && "O e-mail está no formato errado ou não é um e-mail válido"}
            </Alert>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label htmlFor="senha">Senha:</Form.Label>
              <Form.Control
                id="senha"
                type="password"
                className="p-2 mt-2"
                placeholder="Digite sua senha"
                {...register("senha", { required: true, minLength: 6, maxLength: 100 })}
              />
                <Alert variant="white" className={`${errors?.senha? "" : "d-none"} text-danger`}>
                    {!errors.root?.serverError && errors?.senha?.type == "required" &&  "Senha é obrigatória"}
                    {!errors.root?.serverError && errors?.senha?.type == "minLength" && "Senha precisa ter no mínimo 5 caracteres"}
                    {!errors.root?.serverError && errors?.senha?.type == "maxLength" && "Senha precisa ter no máximo 100 caracteres"}
                </Alert>
            </Form.Group>
            <Alert variant="white" className={`${errors?.root?.serverError ? "" : "d-none"} text-danger mb-3`}>
                {errors?.root?.serverError?.message}
            </Alert>

            <Button
              variant="primary"
              type="submit"
              className="w-100 p-2"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Spinner
                    as="span"
                    animation="border"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                    className="me-2"
                  />
                  Entrando...
                </>
              ) : (
                "Entrar"
              )}
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </div>
  );
}
