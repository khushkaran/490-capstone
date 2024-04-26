import React, { useEffect, useState } from 'react'
import { useNavigate } from "react-router-dom";

function ReaderRegistration() {

    const [reader1, setReader1] = useState("")
    const [reader2, setReader2] = useState("")
    const [reader3, setReader3] = useState("")
    const [reader4, setReader4] = useState("")
    const [allReadersRegistered, setAllReadersRegistered] = useState(0)
    const [issueWithPort1, setIssueWithPort1] = useState(0)
    const [issueWithPort2, setIssueWithPort2] = useState(0)
    const [issueWithPort3, setIssueWithPort3] = useState(0)
    const [issueWithPort4, setIssueWithPort4] = useState(0)
    const [changesHaveBeenSaved, setChangesHaveBeenSaved] = useState(0)

    let navigate = useNavigate();
    const readerRoute = () => {
        let path = `/`;
        navigate(path);
    }

    const characterRoute = () => {
        let path = `/characterRegistration`;
        navigate(path);
    }

    const soundRoute = () => {
        let path = `/soundRegistration`;
        navigate(path);
    }

    function checkIfAllReadersRegistered() {
        if (reader1 === "" || reader2 === "" || reader3 === "" || reader4 === "") {
            setAllReadersRegistered(0)
        } else {
            setAllReadersRegistered(1)
        }
    }

    function saveChanges() {
        setIssueWithPort1(0)
        setIssueWithPort2(0)
        setIssueWithPort3(0)
        setIssueWithPort4(0)
        setReader1(document.forms["registerArduinosForm"]["reader1port"].value)
        setReader2(document.forms["registerArduinosForm"]["reader2port"].value)
        setReader3(document.forms["registerArduinosForm"]["reader3port"].value)
        setReader4(document.forms["registerArduinosForm"]["reader4port"].value)

        fetch('http://127.0.0.1:5000/ports', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ "reader1": document.forms["registerArduinosForm"]["reader1port"].value, "reader2": document.forms["registerArduinosForm"]["reader2port"].value, "reader3": document.forms["registerArduinosForm"]["reader3port"].value, "reader4": document.forms["registerArduinosForm"]["reader4port"].value })
        }).then(function (response) {
            if (!response.ok) {
                if (response.status === 401) {
                    setIssueWithPort1(1)
                }
                if (response.status === 402) {
                    setIssueWithPort2(1)
                }
                if (response.status === 403) {
                    setIssueWithPort3(1)
                }
                if (response.status === 404) {
                    setIssueWithPort4(1)
                }
            } else {
                setChangesHaveBeenSaved(1)
            }
        }).catch(error => {
            console.log(error)
        })
    }

    useEffect(() => {
        fetch('http://127.0.0.1:5000/ports', {
            method: 'GET',
        }).then(function (response) {
            return response.json();
        }).then(function (myJson) {
            if (myJson.length > 0) {
                setReader1(myJson[0]["port"])
                setReader2(myJson[1]["port"])
                setReader3(myJson[2]["port"])
                setReader4(myJson[3]["port"])
            }
            checkIfAllReadersRegistered()
            setChangesHaveBeenSaved(0)
        })
    }, [reader1, reader2, reader3, reader4, allReadersRegistered, changesHaveBeenSaved])

    return (
        <div class="readerRegistrationPage">
            <div class='sidebar'>
                <div class="sidebarItem">
                    <button class="sidebarButton" id='readersNav' onClick={() => readerRoute()}>Register Arduinos</button>
                </div>
                <div class="sidebarItem">
                    <button class="sidebarButton" id='charactersNav' onClick={() => characterRoute()}>Register Characters</button>
                </div>
                <div class="sidebarItem">
                    <button class="sidebarButton" id='soundsNav' onClick={() => soundRoute()}>Register Sounds</button>
                </div>
            </div>
            <div class="nonSidebar">
                <h1 key={"header"}>Register Your Arduinos</h1>
                <h3 key={"headerExplanation"}>Please type in the serial port for each Arduino Mega you are using.</h3>
                <form class="registerArduinosForm" name="registerArduinosForm" action={() => { }}>
                    <p>Reader 1</p>
                    <input class="characterNameInput" name="reader1port" defaultValue={reader1} type='text'></input>
                    <p>Reader 2</p>
                    <input class="characterNameInput" name="reader2port" defaultValue={reader2} type='text' />
                    <p>Reader 3</p>
                    <input class="characterNameInput" name="reader3port" defaultValue={reader3} type='text' />
                    <p>Reader 4</p>
                    <input class="characterNameInput" name="reader4port" defaultValue={reader4} type='text' />
                    <p></p>
                    <button class="submitButton" type="button" onClick={() => { saveChanges() }}>Save Changes</button>
                    {/* {changesHaveBeenSaved ? null : <p>{changesHaveBeenSaved}</p>} */}
                </form>
            </div>
            {allReadersRegistered ? (<p>All Arduinos have been registered! Proceed to Register Characters</p>) : <p class="invalidCharacterSubmitted">You have not added a port for all Arduinos yet. Please add a port for all 4 Arduinos and save your changes so you can proceed.</p>}
            {issueWithPort1 ? <p class="invalidCharacterSubmitted">The port you submitted for reader 1 incorrect. Please double check and resubmit.</p> : null}
            {issueWithPort2 ? <p class="invalidCharacterSubmitted">The port you submitted for reader 2 incorrect. Please double check and resubmit.</p> : null}
            {issueWithPort3 ? <p class="invalidCharacterSubmitted">The port you submitted for reader 3 incorrect. Please double check and resubmit.</p> : null}
            {issueWithPort4 ? <p class="invalidCharacterSubmitted">The port you submitted for reader 4 incorrect. Please double check and resubmit.</p> : null}
        </div>
    )
}

export default ReaderRegistration