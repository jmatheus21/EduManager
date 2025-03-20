import React from 'react'
import { Card, Container } from 'react-bootstrap'
import { Cabecalho, Pagina } from "../../components";
import { FaUserTie, FaBook, FaUsers, FaCalendarAlt, FaChalkboardTeacher, FaUserGraduate, FaUserSlash, FaStar, FaDoorOpen, FaClipboardList, FaHistory } from "react-icons/fa";
import { useNavigate } from 'react-router-dom';
import packageJson from "../../../package.json";
import { useAuth } from '../../contexts/AuthContext';

const cards = [
  { "nome": "Usuário", "url": "usuario", "icone": <FaUserTie size={65} color='#000' />, "auth": false },
  { "nome": "Disciplina", "url": "disciplina", "icone": <FaBook size={60} color='#000' />, "auth": false },
  { "nome": "Turma", "url": "turma", "icone": <FaUsers size={70} color='#000' />, "auth": false },
  { "nome": "Calendário", "url": "calendario", "icone": <FaCalendarAlt size={60} color='#000' />, "auth": false },
  { "nome": "Aula", "url": "aula", "icone": <FaChalkboardTeacher size={70} color='#000' />, "auth": false },
  { "nome": "Aluno", "url": "aluno", "icone": <FaUserGraduate size={60} color='#000' />, "auth": false },
  { "nome": "Ausência", "url": "ausencias", "icone": <FaUserSlash size={65} color='#000' />, "auth": true },
  { "nome": "Nota", "url": "nota", "icone": <FaStar size={60} color='#000' />, "auth": true },
  { "nome": "Sala", "url": "sala", "icone": <FaDoorOpen size={70} color='#000' />, "auth": false },
  { "nome": "Boletim", "url": "boletim", "icone": <FaClipboardList size={60} color='#000' />, "auth": false },
  { "nome": "Histórico", "url": "historico", "icone": <FaHistory size={50} color='#000' />, "auth": false },
]

/**
 * Componente para exibir a página inicial.
 * Este componente permite visualizar menu inicial e acessar todas as páginas referentes a cada entidade da aplicação.
 *
 * @returns {JSX.Element} O componente de página inicial.
 */
const HomePage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  return (
    <Pagina>
      <Cabecalho />
      <Container fluid className='d-flex flex-fill justify-content-center align-items-center bg-primary-subtle py-sm-0 py-5'>
        <div className='menu'>
          {
            user && cards.map((card, index) => {
              const disabled = (user.role == "f"? card.auth : !card.auth)

              return (
                <Card key={index} style={{opacity: disabled ? 0.5 : 1, pointerEvents: disabled? "none" : "auto"}} className={`px-5 ${disabled? "bg-secondary" : "custom-card"}`} onClick={() => navigate(card.url)}>
                  <div className="d-flex justify-content-center align-items-center" style={{ height: '120px' }}>
                    {card.icone}
                  </div>
                  <Card.Body>
                    <Card.Title className='text-center text-black pb-4'>{card.nome}</Card.Title>
                  </Card.Body>
                </Card>
              )
            })
          }
        </div>
      </Container>
      <Container fluid>
        <p className='text-center py-3'>EduManager v.{packageJson.version}</p>
      </Container>
    </Pagina>
  )
}

export default HomePage