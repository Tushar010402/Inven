import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  useToast,
} from "@chakra-ui/react";
import axios from 'axios';

const ClientManagement = () => {
  const [clients, setClients] = useState([]);
  const [newClient, setNewClient] = useState({ name: '', contact_email: '', contact_phone: '' });
  const [editingClient, setEditingClient] = useState(null);
  const toast = useToast();

  useEffect(() => {
    fetchClients();
  }, []);

  const fetchClients = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/clients/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
      });
      setClients(response.data);
    } catch (error) {
      console.error('Error fetching clients:', error);
      toast({
        title: "Error fetching clients",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (editingClient) {
      setEditingClient({ ...editingClient, [name]: value });
    } else {
      setNewClient({ ...newClient, [name]: value });
    }
  };

  const handleAddClient = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/clients/', newClient, {
        headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
      });
      setNewClient({ name: '', contact_email: '', contact_phone: '' });
      fetchClients();
      toast({
        title: "Client added successfully",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error adding client:', error);
      toast({
        title: "Error adding client",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const handleUpdateClient = async (e) => {
    e.preventDefault();
    try {
      await axios.put(`http://localhost:5000/api/clients/${editingClient.id}/`, editingClient, {
        headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
      });
      setEditingClient(null);
      fetchClients();
      toast({
        title: "Client updated successfully",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error updating client:', error);
      toast({
        title: "Error updating client",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const handleDeleteClient = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/api/clients/${id}/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
      });
      fetchClients();
      toast({
        title: "Client deleted successfully",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error deleting client:', error);
      toast({
        title: "Error deleting client",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box>
      <Heading as="h2" size="xl" mb={4}>
        Client Management
      </Heading>
      <VStack spacing={4} as="form" onSubmit={editingClient ? handleUpdateClient : handleAddClient}>
        <FormControl isRequired>
          <FormLabel>Client Name</FormLabel>
          <Input
            name="name"
            value={editingClient ? editingClient.name : newClient.name}
            onChange={handleInputChange}
          />
        </FormControl>
        <FormControl isRequired>
          <FormLabel>Contact Email</FormLabel>
          <Input
            name="contact_email"
            type="email"
            value={editingClient ? editingClient.contact_email : newClient.contact_email}
            onChange={handleInputChange}
          />
        </FormControl>
        <FormControl isRequired>
          <FormLabel>Contact Phone</FormLabel>
          <Input
            name="contact_phone"
            value={editingClient ? editingClient.contact_phone : newClient.contact_phone}
            onChange={handleInputChange}
          />
        </FormControl>
        <Button type="submit" colorScheme="blue">
          {editingClient ? 'Update Client' : 'Add Client'}
        </Button>
        {editingClient && (
          <Button onClick={() => setEditingClient(null)} colorScheme="gray">
            Cancel Edit
          </Button>
        )}
      </VStack>
      <Table variant="simple" mt={8}>
        <Thead>
          <Tr>
            <Th>Name</Th>
            <Th>Email</Th>
            <Th>Phone</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {clients.map((client) => (
            <Tr key={client.id}>
              <Td>{client.name}</Td>
              <Td>{client.contact_email}</Td>
              <Td>{client.contact_phone}</Td>
              <Td>
                <Button
                  colorScheme="blue"
                  size="sm"
                  mr={2}
                  onClick={() => setEditingClient(client)}
                >
                  Edit
                </Button>
                <Button
                  colorScheme="red"
                  size="sm"
                  onClick={() => handleDeleteClient(client.id)}
                >
                  Delete
                </Button>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default ClientManagement;
