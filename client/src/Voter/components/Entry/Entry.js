import React, { useState } from 'react'
import { Form, Button } from 'react-bootstrap'
import axios from 'axios'

const SCREEN_SIGN_IN = "SCREEN_SIGN_IN";
const SCREEN_VOTE = "SCREEN_VOTE";


export default ({ handleChangeScreen }) => {
    const [id, setId] = useState("");
    const [password, setPassword] = useState("");
    const server = process.env.REACT_APP_SERVER_URL || '';
    const handleClick = (e) => {
        if (e.target.name === "id") setId(e.target.value);
        else if (e.target.name === "password") setPassword(e.target.value);
    }


    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post(`${server}/sign-in`, {
            voterid: id,
            password
        }).then(res => {
            handleChangeScreen(SCREEN_VOTE)
        }).catch(err => {

        })
    }


    return <div className="container m-5">
        <Form onSubmit={handleSubmit}>
            <Form.Group>
                <Form.Label>Voter ID</Form.Label>
                <Form.Control type="number" name={"id"} placeholder="Enter voter ID" value={id} onChange={handleClick} />
            </Form.Group>
            <Form.Group>
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" name={"password"} placeholder="Password" value={password} onChange={handleClick} />
            </Form.Group>
            <Button variant="primary" type="submit">
                Login
        </Button>
        </Form>
    </div>
}