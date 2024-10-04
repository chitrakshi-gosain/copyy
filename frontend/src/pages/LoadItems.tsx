import {
  Box,
  Button,
  Textarea,
  useToast,
  Heading,
  Flex,
  Icon,
} from '@chakra-ui/react'
import { useState } from 'react'
import axiosInstance from '../utils/axiosInstance'
import { FaCloudUploadAlt } from 'react-icons/fa'
import { useNavigate } from 'react-router-dom'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { solarizedlight } from 'react-syntax-highlighter/dist/esm/styles/prism'

const LoadItems = () => {
  const [jsonInput, setJsonInput] = useState('')
  const [isValid, setIsValid] = useState(true) // State to track validity
  const toast = useToast()
  const navigate = useNavigate() // Initialize useNavigate

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value
    setJsonInput(value)

    // Validate JSON input
    try {
      JSON.parse(value)
      setIsValid(true) // Set to true if JSON is valid
    } catch (error) {
      setIsValid(false) // Set to false if JSON is invalid
    }
  }

  const handleSubmit = async () => {
    try {
      if (jsonInput === '') {
        toast({
          title: 'No input provided',
          status: 'error',
        })
      } else if (!isValid) {
        toast({
          title: 'Invalid JSON provided',
          status: 'error',
        })
      } else {
        const response = await axiosInstance.post('/item', jsonInput, {
          headers: {
            'Content-Type': 'application/json',
          },
        })
        toast({
          title: response.data,
          status: 'success',
        })
        setJsonInput('') // Clear the input field after successful submission
      }
    } catch (error) {
      toast({ title: 'Failed to load items', status: 'error' })
    }
  }

  return (
    <Flex
      direction="column"
      align="center"
      justify="center"
      mt={8}
      p={4}
      minH="80vh"
    >
      <Flex align="center" mb={4}>
        <Icon as={FaCloudUploadAlt} boxSize={10} color="teal.500" />
        <Heading as="h2" size="2xl" ml={2}>
          Load Items
        </Heading>
      </Flex>

      <Textarea
        placeholder="Enter JSON data here..."
        value={jsonInput}
        onChange={handleChange} // Use the new handleChange for validation
        mb={4}
        resize="none" // Optional: Disable resizing
        width="600px" // Set a fixed width
        height="100px" // Set a fixed height
        borderColor={isValid ? 'gray.200' : 'red.500'} // Change border color based on validity
      />

      <Box width="600px" mb={4}>
        <SyntaxHighlighter language="json" style={solarizedlight}>
          {jsonInput}
        </SyntaxHighlighter>
      </Box>

      <Button bg="#66bc82" mt={4} onClick={handleSubmit}>
        Load Items
      </Button>

      {/* Button to navigate to Current Data page */}
      <Button bg="#fbdc6b" mt={4} onClick={() => navigate('/current-data')}>
        View Current Data
      </Button>
    </Flex>
  )
}

export default LoadItems
