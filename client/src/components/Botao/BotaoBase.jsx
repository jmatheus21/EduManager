import { Button } from '@mui/material'
import React from 'react'

const BotaoBase = ({ title, color = 'primary', ...props }) => {
  return (
    <Button variant='contained' color={color} className='py-2 px-3' {...props}>
        { title }
    </Button>
  )
}

export default BotaoBase