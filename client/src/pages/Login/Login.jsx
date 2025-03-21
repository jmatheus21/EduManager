import React from 'react'
import { Container, Navbar } from 'react-bootstrap'
import { Pagina } from "../../components"
import packageJson from "../../../package.json";
import LoginForm from './components/LoginForm';

const Login = () => {
  return (
    <Pagina>
        <Navbar bg="primary" variant="dark" expand="lg" className="p-3">
            <Container fluid>
                <Navbar.Brand className="fs-2 fw-bold">
                    EduManager
                </Navbar.Brand>
            </Container>
        </Navbar>
        <Container fluid className='flex-fill bg-light d-flex justify-content-center align-items-center'>
            <LoginForm />
        </Container>
        <Container fluid className='bg-primary'>
            <p className='text-center py-3 text-white'>EduManager v.{packageJson.version}</p>
        </Container>
    </Pagina>
  )
}

export default Login