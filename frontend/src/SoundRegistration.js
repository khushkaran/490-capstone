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

    function setInitialSoundAssociations() {
        let newJson = {}
        listOfReaders.map((readerItem, readerIndex) => {
            listOfCharacters.map((charItem, charIndex) => {
                let name = `${charItem["name"]}_${readerItem}`
                // fetch('http://127.0.0.1:5000/updateChar', {
                //     method: 'GET',
                //     headers: {
                //         'Content-Type': 'application/json',
                //     },
                //     body: JSON.stringify({ "name": "Taylor" })
                // }).then(function (response) {
                //     return response.json();
                // }).then(function (soundAssociations) {
                //     console.log(soundAssociations)
                // })

                console.log(`${charItem["name"]}--${readerItem}`)

            })
        })
    }

    function getUpdatedSoundAssociations() {  
        listOfCharacters.map((charItem, charIndex) => {
            fetch(`http://127.0.0.1:5000/updateChar/${Object.values(charItem)[0]}`, {
                    method: 'GET'
                }).then(function (response) {
                    return response.json();
                }).then(function (soundAssociations) {
                    console.log(soundAssociations)
                    let newJson = {
                        "name": Object.values(charItem)[0],
                        "reader": soundAssociations["reader"],
                        "soundFile": soundAssociations["soundFile"]
                    }
                    setListOfEntries(listOfEntries => [...listOfEntries, newJson])
                })
        })
    }

    function fileUploaded(charName, readerName, event) {
        const file = event.target.files[0];
        setNewlyUploadedFiles([...newlyUploadedFiles, {
            "prevName": charName,
            "reader": readerName,
            "newName": charName,
            "soundFile": file.name
        }])
        console.log(JSON.stringify(newlyUploadedFiles))
    }

    function submitUploadedFiles() {
        console.log("changes saved")
        // iterate over the array and send the patch requests

        setNewlyUploadedFiles([])
    }

    useEffect(() => {
        fetch('http://127.0.0.1:5000/getAllChar', {
            method: 'GET',
        }).then(function (response) {
            return response.json();
        }).then(function (listOfCharJson) {
            setListOfCharacters(listOfCharJson)
            console.log(`GET call to getAllChar completed, and ${listOfCharacters} stored in listOfCharacters.`)
        })
    }, [])

    useEffect(() => {
        getUpdatedSoundAssociations()
    }, [listOfCharacters])

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
                <table class="soundTable">
                    <thead>
                        <tr>
                            <th class="soundTableHeader">Character</th>
                            <th class="soundTableHeader">Reader</th>
                            <th class="soundTableHeader">Sound File</th>
                        </tr>
                    </thead>
                    {/* {listOfReaders.map((readerItem, readerIndex) => {
                        return (
                            // <table class="soundTable">
                            <tbody className='soundTableBody'>
                                {listOfCharacters.map((item, charIndex) => (
                                    <tr>
                                        <td>{Object.values(item)[0]}</td>
                                        <td>{readerItem}</td>
                                        <td>
                                            <input type="file" onChange={(event) => fileUploaded(Object.values(item)[0], readerItem, event)} />
                                            <button class="submitButton" type="button" onClick={submitUploadedFiles}>Save Changes</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                            // </table>
                        )
                    })} */}
                    {listOfEntries.map((item, charIndex) => {
                        return (
                            <tbody className='soundTableBody'>
                                <tr>
                                    <td>{Object.values(item)[0]}</td>
                                    <td>{Object.values(item)[1]}</td>
                                    <td>
                                        <input type="file" onChange={(event) => fileUploaded(Object.values(item)[0], 'id', event)} />
                                        <button class="submitButton" type="button" onClick={submitUploadedFiles}>Save Changes</button>
                                    </td>
                                </tr>
                            </tbody>
                        )
                    })}
                </table>


                <form class="setCharacterNameForm" name="setCharacterNameForm" action={submitUploadedFiles}>
                    <button class="submitButton" type="button" onClick={submitUploadedFiles}>Save Changes</button>
                </form>

                {listOfCharacters.map((item) => (
                    <div class="characterNameItem">
                        {Object.values(item).map((val) => (
                            <button class="nameButton">{val}</button>
                        ))}
                    </div>
                ))
                }
            </div>
        </div>
    )
}

export default SoundRegistration