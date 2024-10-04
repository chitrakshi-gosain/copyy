import React from 'react'
import ReactDOM from 'react-dom/client'
import { ChakraProvider, CSSReset } from '@chakra-ui/react'
import { Global } from '@emotion/react'
import App from './App'

const GlobalStyles = () => (
  <Global
    styles={`
      body {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        overflow-x: hidden; /* Prevent horizontal scrollbar */
      }
    `}
  />
)

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
root.render(
  <ChakraProvider>
    <CSSReset />
    <GlobalStyles />
    <App />
  </ChakraProvider>
)
