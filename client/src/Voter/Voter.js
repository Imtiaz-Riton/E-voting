import React, { useState } from 'react';
import { Button, ButtonGroup, Form, ListGroup, Card, ListGroupItem } from 'react-bootstrap';
import aaa from "./aaa.jpg";
import bbb from "./bbb.jpg";
import ccc from "./ccc.jpg";

export default () => {

    const [role, changRole] = useState("none");


    const handleChange = (e) => {

    }

    return (
        <Form>
            <Form.Group controlId="formBasicEmail">
                <Form.Label>Key</Form.Label>
                <Form.Control type="email" placeholder="Enter Your Key" />
            </Form.Group>


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
                                <Form.Check type="checkbox" label="vote me" />
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
                                <Form.Check type="checkbox" label="vote me" />
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
                                <Form.Check type="checkbox" label="vote me" />
                            </Form.Group>
                        </Card>
                    </div>
                </div>
            </div>

            <Button className="mt-3 ml-3" variant="primary" type="submit">
                Submit Your Vote
            </Button>
        </Form>
    );
}

