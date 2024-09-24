import React, { useState } from 'react';
import { ChakraProvider, Box, VStack, Grid, theme, Heading, Tabs, TabList, TabPanels, Tab, TabPanel } from "@chakra-ui/react"
// import { ColorModeSwitcher } from "./ColorModeSwitcher"
import Auth from './components/Auth';
import ClientManagement from './components/ClientManagement';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  return (
    <ChakraProvider theme={theme}>
      <Box textAlign="center" fontSize="xl">
        <Grid minH="100vh" p={3}>
          {/* <ColorModeSwitcher justifySelf="flex-end" /> */}
          <VStack spacing={8}>
            <Heading as="h1" size="2xl">
              Inventory Management System
            </Heading>
            {!isAuthenticated ? (
              <Auth onLogin={handleLogin} />
            ) : (
              <Box width="100%">
                <Heading as="h2" size="xl" mb={4}>
                  Welcome to the Dashboard
                </Heading>
                <Tabs>
                  <TabList>
                    <Tab>Client Management</Tab>
                    {/* Add more tabs for other components */}
                  </TabList>
                  <TabPanels>
                    <TabPanel>
                      <ClientManagement />
                    </TabPanel>
                    {/* Add more TabPanels for other components */}
                  </TabPanels>
                </Tabs>
              </Box>
            )}
          </VStack>
        </Grid>
      </Box>
    </ChakraProvider>
  );
}

export default App;
