import React from 'react'
import { Button, Heading, Text, VStack, useToast } from '@chakra-ui/react'
import { Link, useNavigate } from 'react-router-dom'
import axiosInstance from '../utils/axiosInstance'

const Home: React.FC = () => {
  const toast = useToast()
  const navigate = useNavigate()

  const handleReset = async () => {
    try {
      await axiosInstance.delete('/clear')

      toast({
        title: 'Success!',
        description: 'System state has been reset.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })

      navigate('/')
    } catch (error) {
      toast({
        title: 'Error!',
        description: 'Failed to reset the system state.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  }

  const handleAutoPopulate = async () => {
    try {
      await axiosInstance.post('/load')

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

  return (
    <VStack spacing={8} mt={10}>
      <Heading size="2xl">QuoteCheck Code Challenge</Heading>

      <Text fontSize="lg" textAlign="center">
        Choose an option to get started:
      </Text>

      <VStack spacing={4}>
        <Link to="/load-items">
          <Button
            bg="#66bc82"
            size={{ base: 'md', md: 'lg' }}
            width={{ base: '150px', md: '200px' }}
          >
            Load Data
          </Button>
        </Link>

        <Link to="/match-items">
          <Button
            bg="#47c2dd"
            size={{ base: 'md', md: 'lg' }}
            width={{ base: '150px', md: '200px' }}
          >
            Find the Best Match
          </Button>
        </Link>

        <Link to="/current-data">
          <Button
            bg="#fbdc6b"
            size={{ base: 'md', md: 'lg' }}
            width={{ base: '150px', md: '200px' }}
          >
            View Current Data
          </Button>
        </Link>

        <Button
          bg="#f19f16"
          size={{ base: 'md', md: 'lg' }}
          width={{ base: '150px', md: '200px' }}
          onClick={handleAutoPopulate}
        >
          Auto Populate
        </Button>

        <Button
          bg="#f63130"
          size={{ base: 'md', md: 'lg' }}
          width={{ base: '150px', md: '200px' }}
          onClick={handleReset}
        >
          Reset
        </Button>
      </VStack>
    </VStack>
  )
}

export default Home
