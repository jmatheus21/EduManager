import React from 'react'

const estilo = {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column"
}

/**
 * Componente para padronizar as páginas.
 * Este componente permite padronizar todos os estilos das páginas.
 *
 * @returns {JSX.Element} O componente de página.
 */
const Pagina = ({children}) => {
  return (
    <div className='page' style={estilo}>
        {children}
    </div>
  )
}

export default Pagina