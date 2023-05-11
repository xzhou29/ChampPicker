import React, { useState, useRef, useEffect} from 'react';
import { Container, Row, Col, Dropdown, FormControl, Button, Card } from 'react-bootstrap';
import CardGroup from 'react-bootstrap/CardGroup';
import TeamColumn from './TeamColumn'
import ResultPredictionColumn from './ResultPredictionColumn'
import axios from 'axios';
import initialChampionData from './initialChampionData'

function ChampPickerPage() {
  const [gameVersion, setGameVersion] = useState('13.9');
  const [teamOneWinRate, setTeamOneWinRate] = useState('50.0');
  const [teamTwoWinRate, setTeamTwoWinRate] = useState('50.0');
  const [selections, setSelections] = useState({});
  const [championData, setChampionData] = useState(initialChampionData);
  const [championDataOne, setChampionDataOne] = useState();
  const [championDataTwo, setChampionDataTwo] = useState();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (Object.keys(selections).length === 0) {
        fetch(
            'http://localhost:3000/api/initial_data', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(gameVersion)
            }
        )
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {      // data is the JSON response from your API
          setChampionData(data.champDataAny)
        })
        .catch(error => {
          console.error('There has been a problem with your fetch operation:', error);
        });
        return
    }
    // axios.post('/api/'+'champ_picker?team=${team}&name=${name}&lane=${lane}')
    // fetch(`http://localhost:3000/api/champ_picker?selections=${selections}`
    fetch(
        'http://localhost:3000/api/champ_picker', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(selections)
        }
    )
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {      // data is the JSON response from your API
      setTeamOneWinRate(data.teamOneWinRate);
      setTeamTwoWinRate(data.teamTwoWinRate);
      //setChampionDataOne(data.teamOneChampPicks);
      //setChampionDataTwo(data.teamTwoChampPicks);
    })
    .catch(error => {
      console.error('There has been a problem with your fetch operation:', error);
    });
  }, [selections]);

  const handleImageClickForData = (teamOn) => {
    console.log(teamOn)
//    if (teamOn == 'Team 1') {
//        if (championDataOne !== undefined && championDataOne !== null) {
//            setChampionData(championDataOne);
//        }
//    } else  {
//        if (championDataTwo !== undefined && championDataTwo !== null) {
//            setChampionData(championDataTwo);
//        }
//    }
  };

  const handleChange = (team, name, lane, prevName) => {
    if (name == 'N/A'){
      return;
    }
    if (name == 'Removed'){
        // remove element
        const key = prevName + '@' + team;
        // Remove a key-value pair
        handleDeleteSelection(key)
    }
    else {
       // remove element
        const key = name + '@' +  team;
        // Remove a key-value pair
        handleAddSelection(key, [team, name, lane]);
    }
  }
  // Some code that updates selections, e.g.:
  const handleAddSelection = (key, value) => {
    setSelections({ ...selections, [key]: value });
  };

  const handleDeleteSelection = (key) => {
    const { [key]: deletedKey, ...rest } = selections;
    setSelections(rest);
  };

  return (
    <Container>
      <Row>
        <Col lg={4} >
                <TeamColumn teamName={'Team 1'} handleChange={handleChange}
                            handleImageClickForData={handleImageClickForData}
                            championData={championData}/>
        </Col>

        <Col lg={4} className="text-center">
            <ResultPredictionColumn teamOneWinRate={teamOneWinRate} teamTwoWinRate={teamTwoWinRate} />
        </Col>


        <Col lg={4} className="text-right">
                <TeamColumn teamName={'Team 2'} handleChange={handleChange}
                        championData={championData}
                        handleImageClickForData={handleImageClickForData}
                        cardRowClassName={"justify-content-end"} />
        </Col>
      </Row>

      <div className="text-center">
        <h5> League of Legend - Version <span> {gameVersion} </span> </h5>
      </div>
    </Container>
  );
}

export default ChampPickerPage;