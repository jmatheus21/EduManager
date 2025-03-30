import { FaUserTie, FaBook, FaUsers, FaCalendarAlt, FaChalkboardTeacher, FaUserGraduate, FaUserSlash, FaStar, FaDoorOpen, FaClipboardList, FaHistory } from "react-icons/fa";

const cards = [
  { "nome": "Usuário", "url": "usuario", "icone": <FaUserTie size={30} color='#fff' />, "auth": false },
  { "nome": "Disciplina", "url": "disciplina", "icone": <FaBook size={30} color='#fff' />, "auth": false },
  { "nome": "Turma", "url": "turma", "icone": <FaUsers size={30} color='#fff' />, "auth": false },
  { "nome": "Calendário", "url": "calendario", "icone": <FaCalendarAlt size={30} color='#fff' />, "auth": false },
  { "nome": "Aula", "url": "aula", "icone": <FaChalkboardTeacher size={30} color='#fff' />, "auth": false },
  { "nome": "Aluno", "url": "aluno", "icone": <FaUserGraduate size={30} color='#fff' />, "auth": false },
  { "nome": "Ausência", "url": "ausencias", "icone": <FaUserSlash size={30} color='#fff' />, "auth": true },
  { "nome": "Nota", "url": "nota", "icone": <FaStar size={30} color='#fff' />, "auth": true },
  { "nome": "Sala", "url": "sala", "icone": <FaDoorOpen size={30} color='#fff' />, "auth": false },
  { "nome": "Boletim", "url": "boletim", "icone": <FaClipboardList size={30} color='#fff' />, "auth": false },
  { "nome": "Histórico", "url": "historico", "icone": <FaHistory size={30} color='#fff' />, "auth": false },
  { "nome": "Matrícula", "url": "matricula", "icone": <FaUserGraduate size={30} color='#fff' />, "auth": false }
]

export default cards;