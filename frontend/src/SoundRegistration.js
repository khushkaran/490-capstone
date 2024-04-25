import React, { useEffect, useState } from 'react'
import { useNavigate } from "react-router-dom";

function SoundRegistration() {
    const [listOfCharacters, setListOfCharacters] = useState([])
    const [listOfReaders, setListOfReaders] = useState([])
    const [newlyUploadedFiles, setNewlyUploadedFiles] = useState([])
    const [existingAssociations, setExistingAssociations] = useState({})
    const [listOfEntries, setListOfEntries] = useState([])
    const [doneRefreshing, setDoneRefreshing] = useState(0)

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

    function fileUploaded(charName, readerName, event) {
        const file = event.target.files[0];

        setNewlyUploadedFiles([...newlyUploadedFiles, {
            "prevName": charName,
            "reader": readerName,
            "newName": charName,
            "soundFile": "/Users/thakshamangalam/Documents/490-capstone/" + file.name

        }])
    }


    function submitUploadedFiles() {
        // iterate over the array and send the patch requests
        newlyUploadedFiles.map((reqToSend, reqToSendIndex) => {
            fetch(`http://127.0.0.1:5000/updateChar`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                body: JSON.stringify(reqToSend)
            }).then(function (response) {
                if (!response.ok) {
                    console.log(`There is an issue with the request.`)
                }
            }).catch(error => {
                console.log(error)
            })
        })

        setDoneRefreshing(1)
        setNewlyUploadedFiles([])
    }

    useEffect(() => {
        fetch('http://127.0.0.1:5000/getAllChar', {
            method: 'GET',
        }).then(function (response) {
            return response.json();
        }).then(function (listOfCharJson) {
            setListOfCharacters(listOfCharJson)
            setDoneRefreshing(0)
        })
    }, [doneRefreshing])

    return (
        <div class="soundRegistrationPage">
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
                <h1 key={"header"}>Add Sounds to Characters</h1>
                <h3 key={"headerExplanation"}>Choose a sound file for your character-reader pairs! If you don't want any sound, just don't select a file. You can overwrite your old sound file by choosing a new file. Remember to save your changes!</h3>
                {(listOfCharacters.length === 0) ? <p>You have not registered any characters. Please register your characters and return to this page.</p> : <table class="soundTable">
                    <thead>
                        <tr>
                            <th class="soundTableHeader">Character</th>
                            <th class="soundTableHeader">Reader</th>
                            <th class="soundTableHeader">Sound File</th>
                        </tr>
                    </thead>
                    {listOfCharacters.map((item, charIndex) => {
                        return (
                            <tbody className='soundTableBody'>
                                <tr>
                                    <td>{item.name}</td>
                                    <td>{item.reader}</td>
                                    <td>{item.soundFile ? (
                                        <div class="soundFileBox">
                                            <p class="soundFileName">{item.soundFile}</p>
                                            <input type="file" accept=".mp3" onChange={(event) => fileUploaded(item.name, item.reader, event)} />
                                        </div>
                                    ) : <input type="file" accept=".mp3" onChange={(event) => fileUploaded(item.name, item.reader, event)} />}</td>
                                </tr>
                            </tbody>
                        )
                    })}
                </table>}
                <div class="submitButtonContainer">
                    <button class="submitButton" type="button" onClick={submitUploadedFiles}>Save Changes</button>
                </div>

            </div>
        </div>
    )
}

export default SoundRegistration