import React from 'react'
import { Container } from 'react-bootstrap'

const BotaoGroup = ({ children }) => {
  return (
    <Container fluid className='d-flex gap-3 justify-content-end align-items-center my-3 mt-auto'>
        { children }
    </Container>
  )
}

export default BotaoGroup