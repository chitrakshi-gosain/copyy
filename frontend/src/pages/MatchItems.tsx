import React, { useState } from 'react'
import {
  Box,
  Input,
  Button,
  useToast,
  Flex,
  Text,
  VStack,
  Icon,
} from '@chakra-ui/react'
import { FaTimesCircle } from 'react-icons/fa' // Import the cross icon
import axiosInstance from '../utils/axiosInstance'

const MatchItems: React.FC = () => {
  const [trade, setTrade] = useState('')
  const [unitOfMeasure, setUnitOfMeasure] = useState('')
  const [match, setMatch] = useState<{
    best_match: {
      trade: string
      unit_of_measure: string
      rate: number
      id: string
    }
    similarity_score: number
  } | null>(null) // State for storing match
  const toast = useToast()

  const handleSubmit = async () => {
    try {
      const response = await axiosInstance.post('/match/item', {
        trade,
        unit_of_measure: unitOfMeasure,
      })
      setMatch({
        best_match: response.data.best_match,
        similarity_score: response.data.similarity_score,
      }) // Update match state
    } catch (error) {
      toast({ title: 'No matching item found', status: 'error' })
      setMatch(null) // Clear match if there's an error
    }
  }

  return (
    <Box p={4} flex="1">
      <Text fontSize="3xl" mb={6}>
        Find Best Match
      </Text>
      <Flex direction="column" gap={4}>
        <Input
          placeholder="Enter trade"
          value={trade}
          onChange={(e) => setTrade(e.target.value)}
        />
        <Input
          placeholder="Enter unit of measure"
          value={unitOfMeasure}
          onChange={(e) => setUnitOfMeasure(e.target.value)}
        />
        <Button colorScheme="green" onClick={handleSubmit}>
          Find Match
        </Button>
      </Flex>

      {/* Match Card */}
      {match && (
        <Box
          mt={6}
          p={4}
          borderWidth={1}
          borderRadius="md"
          bg="green.50"
          boxShadow="lg"
        >
          <VStack align="center">
            <Text fontSize="5xl" fontWeight="bold" color="green.800">
              Best Match has a similarity score of {match.similarity_score}
            </Text>
            <Box
              key={match.best_match.id}
              p={12} // Keep this as is to ensure card size
              borderWidth="1px"
              borderRadius="lg"
              boxShadow="lg"
              textAlign="center"
              bg="#F5F1E6"
              height="250px" // Set height for card
              color="green.500"
            >
              <Text fontSize="4xl" fontWeight="bold">
                Trade: {match.best_match.trade}
              </Text>
              <Text fontSize="2xl">
                Unit: {match.best_match.unit_of_measure}
              </Text>
              <Text fontSize="xl">
                Rate: ${match.best_match.rate.toFixed(2)}
              </Text>
            </Box>
          </VStack>
        </Box>
      )}

      {/* No Match Found Card */}
      {match === null && (
        <Box
          mt={6}
          p={4}
          borderWidth={1}
          borderRadius="md"
          bg="red.50"
          boxShadow="lg"
        >
          <VStack align="center">
            <Icon as={FaTimesCircle} boxSize={12} color="red.500" />{' '}
            {/* Cross Icon */}
            <Text fontSize="5xl" fontWeight="bold" color="red.800">
              No Match Found
            </Text>
            <Text fontSize="3xl" color="red.600">
              Please try a different criteria.
            </Text>
          </VStack>
        </Box>
      )}
    </Box>
  )
}

export default MatchItems
