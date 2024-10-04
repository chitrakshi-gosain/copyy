import React from 'react'
import { Box, Flex, Icon, Text, useBreakpointValue } from '@chakra-ui/react'
import { FaHome } from 'react-icons/fa'
import { Link } from 'react-router-dom'

const RootLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Use a breakpoint value for different font sizes in the header
  const headerFontSize = useBreakpointValue({ base: 'lg', md: 'xl' })

  return (
    <Box minH="100vh" display="flex" flexDirection="column" p={0}>
      {/* Header */}
      <Box w="100%" bg="teal.500" p={4} color="white">
        <Flex align="center" justify="space-between">
          <Link to="/">
            <Icon as={FaHome} boxSize={8} cursor="pointer" />
          </Link>
          <Text fontSize={headerFontSize}>QuoteCheck</Text>
        </Flex>
      </Box>

      {/* Main Content */}
      <Box as="main" flex="1" w="100%" p={4} overflowY="auto">
        {' '}
        {/* Enable vertical scrolling */}
        {children}
      </Box>

      {/* Footer */}
      <Box as="footer" w="100%" bg="teal.500" p={4} color="white">
        <Text textAlign="center">© 2024 QuoteCheck. All rights reserved.</Text>
      </Box>
    </Box>
  )
}

export default RootLayout
