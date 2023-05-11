import React, { useState, useRef, useEffect } from 'react';
import { Container, Row, Col, Dropdown, FormControl, Button, Card, Modal, Form, DropdownButton, Table } from 'react-bootstrap';
import CardGroup from 'react-bootstrap/CardGroup';
//import championData from './championData';
import '../public/css/style.css';

function ChampionCard({ champion, teamName, handleChange, handleImageClickForData,  championData}) {
  const [image, setImage] = useState(champion.IconImageLink);
  const [name, setName] = useState(champion.champName);
  const [prevName, setPrevName] = useState();
  const [team, setTeam] = useState(teamName);
  const [lane, setLane] = useState('Lane');
  const [showModal, setShowModal] = useState(false);
  const [showDeleteButton, setDeleteButton] = useState(false)
  const [searchText, setSearchText] = useState('');
  const isFirstRender = useRef(true);
  const lanes = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'SUPPORT'];

  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }else{
      handleChange(team, name, lane, prevName)
    }
  }, [team, name, lane]);

  const handleLaneSelection = (lane) => {
    setLane(lane);
  };

  const handleDeleteImage = () => {
    setImage('/images/select.png');
    setDeleteButton(false);
    setName('Removed');
    setPrevName(name)
  };

  const handleImageClick = () => {
    handleImageClickForData(team)
    setShowModal(true);
  };

  const handleSelectChampion = (index, champion) => {
    setImage(champion.iconImageLink);
    setName(champion.champName);
    setShowModal(false);
    setDeleteButton(true);
  };

  // Filter the champions based on the search text
  const filteredChampions = championData.filter((champion) =>
    champion.champName.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
  <div>
    <Card style={{ width: '6rem' }} >
      <Card.Img
        variant="top"
        src={image}
        onClick={handleImageClick}
      />
      {champion.IconImageLink && (
        <Button
          variant="danger"
          size="sm"
          style={{ position: 'absolute', top: 0, right: 0, display: showDeleteButton ? 'block' : 'none' }}
          onClick={handleDeleteImage}
        >
          X
        </Button>
      )}
      <Card.Body style={{ padding: '0rem' }} >
        <DropdownButton
          id="lane-dropdown"
          title={lane}
          onSelect={handleLaneSelection}
        >
              <Dropdown.Item eventKey="Top">Top</Dropdown.Item>
              <Dropdown.Item eventKey="Jungle">Jungle</Dropdown.Item>
              <Dropdown.Item eventKey="Middle">Middle</Dropdown.Item>
              <Dropdown.Item eventKey="Bottom">Bottom</Dropdown.Item>
              <Dropdown.Item eventKey="Support">Support</Dropdown.Item>
              <Dropdown.Item eventKey="Lane">Any Lane</Dropdown.Item>
        </DropdownButton>

        <Card.Title style={{ fontSize: '1rem', marginBottom: '1.5rem' }} >
            {name}
        </Card.Title>

      </Card.Body>
    </Card>

    <Modal show={showModal} onHide={() => setShowModal(false)}  size="xl" >

        <Modal.Header closeButton>
          <Modal.Title>Select a Champion</Modal.Title>
        </Modal.Header>
        <Modal.Body>

          <Form.Group>
            <Form.Control
              type="text"
              placeholder="Search Champions"
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
            />
          </Form.Group>

          <div className="row" style={{ margin: '3rem'}}>
            {lanes.map((lane) => {
              // Filter the champions for the current lane
              const newFilteredChampions = filteredChampions.filter((champion) => champion.laneName === lane);
              // Map the filtered data into a column
              return (
                <div style={{ width: '20%'}} key={lane} >
                  <h4>{lane}</h4>
                  {newFilteredChampions
                  .sort((a, b) => b.winRate - a.winRate)
                  .map((champion, index) => (
                    <div key={`${champion.winRate}-${champion.champName}`}
                      onClick={() => handleSelectChampion(index, champion)}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        padding: '0.0rem',
                        cursor: 'pointer',
                      }}
                    >
                      <img src={champion.iconImageLink}
                           alt={champion.champName}
                           style={{ width: '2rem', margin: '0.1rem' }} />
                      <span style={{ marginLeft: '0.3rem' }}> {champion.winRate}% - {champion.champName} </span>
                    </div>
                  ))}
                </div>
              );
            })}
          </div>
        </Modal.Body>
      </Modal>
  </div>
  );
}

function TeamColumn( {cardRowClassName, teamName, handleChange, championData, handleImageClickForData} ) {
    // initialize number of spots
    const champions = [
      {
        champName: 'N/A',
        laneName: 'Lane',
        IconImageLink: './public/images/select.png',
      },
      {
        champName: 'N/A',
        laneName: 'Lane',
        IconImageLink: './public/images/select.png',
      },
      {
        champName: 'N/A',
        laneName: 'Lane',
        IconImageLink: './public/images/select.png',
      },
      {
        champName: 'N/A',
        laneName: 'Lane',
        IconImageLink: './public/images/select.png',
      },
      {
        champName: 'N/A',
        laneName: 'Lane',
        IconImageLink: './public/images/select.png',
      },
    ];
    return (
        <div>
            <h4> {teamName} </h4>
            {champions.map((champion, index) => (
              <Row  key={index} className={cardRowClassName}>
                <ChampionCard  champion={champion} teamName={teamName}
                                handleChange={handleChange} handleImageClickForData={handleImageClickForData}
                               championData={championData}
                />
              </Row>
            ))}
        </div>
    );
}

export default TeamColumn;


//       {filteredChampions.map((champion, index)  => (
//            <div
//              key={champion.champName}
//              onClick={() => handleSelectChampion(index, champion)}
//              style={{
//                display: 'flex',
//                alignItems: 'center',
//                padding: '0.5rem',
//                cursor: 'pointer',
//              }}
//            >
//              <img
//                src={champion.iconImageLink}
//                alt={champion.champName}
//                style={{ width: '2rem', marginRight: '1rem' }}
//              />
//              <div>
//                {champion.champName} ({champion.winRate})
//              </div>
//            </div>
//          ))}