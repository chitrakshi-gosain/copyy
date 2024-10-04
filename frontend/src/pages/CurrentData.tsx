// pages/CurrentData.tsx
import React, { useEffect, useState } from 'react'
import {
  Box,
  Text,
  Spinner,
  SimpleGrid,
  Button,
  Flex,
  useToast,
} from '@chakra-ui/react'
import axiosInstance from '../utils/axiosInstance'

interface Item {
  id: string
  trade: string
  unit_of_measure: string
  rate: number
}

const CurrentData: React.FC = () => {
  const toast = useToast()
  const [items, setItems] = useState<Item[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)
  const [currentPage, setCurrentPage] = useState<number>(1)

  // Fetch items function
  const fetchItems = async () => {
    try {
      const response = await axiosInstance.get('/item')
      setItems(response.data)
    } catch (err: any) {
      setError(err.message || 'An error occurred while fetching items')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchItems() // Call the fetchItems function when the component mounts
  }, [])

  // Determine the number of items per page
  const PAGE_SIZE = items.length < 6 ? items.length : 6
  const totalPages = Math.ceil(items.length / PAGE_SIZE)
  const startIndex = (currentPage - 1) * PAGE_SIZE
  const endIndex = startIndex + PAGE_SIZE
  const currentItems = items.slice(startIndex, endIndex)

  const handlePageChange = (page: number) => {
    setCurrentPage(page)
  }

  const handleAutoPopulate = async () => {
    try {
      await axiosInstance.post('/load')
      // Fetch items again after auto-populating
      await fetchItems()

      toast({
        title: 'Success!',
        description: 'Data has been auto populated.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
    } catch (error) {
      toast({
        title: 'Error!',
        description: 'Failed to auto populate data.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  }

  if (loading) {
    return (
      <Box textAlign="center" mt={8}>
        <Spinner size="xl" />
      </Box>
    )
  }

  if (error) {
    return (
      <Box textAlign="center" mt={8}>
        <Text color="red.500">Error: {error}</Text>
      </Box>
    )
  }

  if (items.length === 0) {
    return (
      <Flex
        align="center"
        justify="center"
        direction="column"
        height="80vh" // Full height of 80% of the viewport
        textAlign="center"
      >
        <Text fontSize="7xl" color="gray.500">
          The system has no data 😔
        </Text>
        <Text fontSize="3xl">Please load some items to get started.</Text>
        <Button
          colorScheme="yellow"
          size={{ base: 'md', md: 'lg' }}
          width={{ base: '150px', md: '200px' }}
          onClick={handleAutoPopulate}
          mt={4} // Add margin-top for spacing
        >
          Auto Populate
        </Button>
      </Flex>
    )
  }

  return (
    <Box p={4} pb={0} maxH="80vh" overflowY="auto" height="80vh" flex="1">
      <Text fontSize="2xl" mb={4}>
        Current Data
      </Text>
      <SimpleGrid columns={{ base: 1, sm: 2, md: 3 }} spacing={4}>
        {currentItems.map((item) => (
          <Box
            key={item.id}
            p={12} // Keep this as is to ensure card size
            borderWidth="1px"
            borderRadius="lg"
            boxShadow="lg"
            textAlign="center"
            bg="white"
            height="225px" // Set height for card
          >
            <Text fontSize="4xl" fontWeight="bold">
              Trade: {item.trade}
            </Text>
            <Text fontSize="2xl">Unit: {item.unit_of_measure}</Text>
            <Text fontSize="xl">Rate: ${item.rate.toFixed(2)}</Text>
          </Box>
        ))}
      </SimpleGrid>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <Box mt={4} mb={4}>
          {' '}
          {/* Add margin top and bottom for spacing */}
          <Flex justifyContent="space-between">
            <Button
              onClick={() => handlePageChange(currentPage - 1)}
              isDisabled={currentPage === 1}
            >
              Previous
            </Button>
            <Text>
              Page {currentPage} of {totalPages}
            </Text>
            <Button
              onClick={() => handlePageChange(currentPage + 1)}
              isDisabled={currentPage === totalPages}
            >
              Next
            </Button>
          </Flex>
        </Box>
      )}
    </Box>
  )
}

export default CurrentData
