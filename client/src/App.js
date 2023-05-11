import React from 'react';
import ChampPickerPage from './ChampPickerPage';
import Header from './Header'
import { Container, Row, Col } from 'react-bootstrap';


const App = () => {

  const containerStyle = {
    backgroundColor: '#f8f9fa' // replace with your desired color
  };


  return (
    <Container style={containerStyle}>
        <ChampPickerPage />
    </Container>
  );
};

export default App;