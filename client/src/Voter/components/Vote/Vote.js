import React, { useState } from 'react';
import { Button, ButtonGroup, Form, ListGroup, Card, ListGroupItem } from 'react-bootstrap';
import aaa from "../../aaa.jpg";
import bbb from "../../bbb.jpg";
import ccc from "../../ccc.jpg";
import axios from 'axios'

export default () => {

    const [c1, setC1] = useState(false);
    const [c2, setC2] = useState(false);
    const [c3, setC3] = useState(false);
    const [value, setValue] = useState(0);
    const server = process.env.REACT_APP_SERVER_URL || '';

    const handleChange = (v) => {
        setC1(false);
        setC2(false);
        setC3(false);

        switch (v) {
            case 1: setC1(true);
                setValue(1);
                break;
            case 2: setC2(true);
                setValue(2);
                break;
            case 3: setC3(true);
                setValue(3);
                break;
        }

    }

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post(`${server}/vote`, {
            candidate: value
        }).then(res => {
            console.log(res.data)
        }).catch(err => {

        })
    }
    return (
        <Form className="mt-4" onSubmit={handleSubmit}>
            <div className="container">
                <div className="row">
                    <div className="col">
                        <Card style={{ width: '18rem' }}>
                            <Card.Img variant="top" src={aaa} />
                            <Card.Body>
                                <Card.Title>Donald Trump</Card.Title>
                                <Card.Text>
                                    Donald John Trump is the 45th and current president of the United States. Before entering politics.
                            </Card.Text>
                            </Card.Body>

                            <Form.Group controlId="formBasicCheckbox" className="ml-3">
                                <Form.Check type="checkbox" name="c1" checked={c1} onChange={() => handleChange(1)} />
                            </Form.Group>
                        </Card>
                    </div>
                    <div className="col">
                        <Card style={{ width: '18rem' }}>
                            <Card.Img variant="top" src={bbb} />
                            <Card.Body>
                                <Card.Title>Joe Biden</Card.Title>
                                <Card.Text>
                                    Joseph Robinette Biden Jr. is an American politician who served as the 47th vice president of the United States from 2009 to 2017
                             </Card.Text>
                            </Card.Body>


                            <Form.Group controlId="formBasicCheckbox" className="ml-3">
                                <Form.Check type="checkbox" name="c2" checked={c2} onChange={() => handleChange(2)} />
                            </Form.Group>
                        </Card>
                    </div>
                    <div className="col">
                        <Card style={{ width: '18rem' }}>
                            <Card.Img variant="top" src={ccc} />
                            <Card.Body>
                                <Card.Title>Barack  Obama</Card.Title>
                                <Card.Text>
                                    Barack Hussein Obama II is an American politician and attorney who served as the 44th president of the United States
                             </Card.Text>
                            </Card.Body>


                            <Form.Group controlId="formBasicCheckbox" className="ml-3">
                                <Form.Check type="checkbox" name="c3" checked={c3} onChange={() => handleChange(3)} />
                            </Form.Group>
                        </Card>
                    </div>
                </div>
            </div>
            <div className="container">
                <Button className="mt-3" variant="primary" type="submit">
                    Submit Your Vote
            </Button>
            </div>
        </Form>
    );
}

