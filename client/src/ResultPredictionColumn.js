import React, { useState } from 'react';
import { Row, Col } from 'react-bootstrap';
//import CardGroup from 'react-bootstrap/CardGroup';
//import championData from './championData';
//import '../public/css/style.css';


function ResultPredictionColumn( {teamOneWinRate, teamTwoWinRate}) {
    return (
    <div>
        <h4 style={{ marginBottom: '1rem' }}>  Predicted Win Rate </h4>
        <Row>
            <Col lg={6}>
            <h4> Team 1: </h4>
            <p> {teamOneWinRate}% </p>
            </Col>

            <Col lg={6}>
            <h4> Team 2: </h4>
            <p> {teamTwoWinRate}% </p>
            </Col>
        </Row>
        <h3  > Recommendations: </h3>
    </div>
    )
}

export default ResultPredictionColumn;