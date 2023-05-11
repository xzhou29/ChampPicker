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
            <h4> Team 1 </h4>
            <h5> {teamOneWinRate}% </h5>
            </Col>

            <Col lg={6}>
            <h4> Team 2 </h4>
            <h5> {teamTwoWinRate}% </h5>
            </Col>
        </Row>
        <div className='text-left' style={{margin: '1rem'}}>
           <h5> Data Facts: </h5>
            <p> (1) Our dataset consists of the 40 most recent games played by all players ranked Diamond II or higher.
                    The dataset is updated daily.</p>
            <p> (2) Our win rate prediction model uses team composition data from all ranked games played at Diamond II and above.
                    The model is updated daily to ensure the latest data is used. </p>
        </div>

    </div>
    )
}

export default ResultPredictionColumn;