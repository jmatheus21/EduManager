import React from 'react'

/**
 * Componente para exibir o título interno.
 * Este componente permite visualizar o título das páginas.
 *
 * @returns {JSX.Element} O componente de título.
 */
const Titulo = ({children}) => {
  return (
    <h2 className="fw-bold">{children}</h2>
  )
}

export default Titulo