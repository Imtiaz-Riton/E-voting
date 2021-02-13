import React, { useState } from 'react';
import { Button, ButtonGroup } from 'react-bootstrap';
import Voter from './Voter/Voter';

import Entry from './Voter/components/Entry/Entry'
import Vote from './Voter/components/Vote/Vote'
const SCREEN_SIGN_IN = "SCREEN_SIGN_IN";
const SCREEN_VOTE = "SCREEN_VOTE";

function App() {

  const [screen, setScreen] = useState(SCREEN_SIGN_IN);

  const handleChangeScreen = (s) => {
    setScreen(s);
  }


  return (
    screen === SCREEN_SIGN_IN ? <Entry handleChangeScreen={handleChangeScreen} /> : <Vote />
    // <div className="container">
    //   <div className="row">
    //     <div className="container">
    //       <div className="container mt-5">
    //         <h4>Choose A Role</h4>
    //       </div>
    //     </div>
    //     <div className="container ml-3 mt-5">
    //       <ButtonGroup aria-label="Basic example">
    //         <Button variant="secondary" size={"lg"}>Voter</Button>
    //         <Button variant="primary">Miner</Button>
    //       </ButtonGroup>
    //       <Voter />
    //     </div>
    //   </div>
    // </div >
  );
}

export default App;
