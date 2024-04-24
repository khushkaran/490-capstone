import React, { useEffect, useState } from 'react'

function SoundRegistration() {

    const [listOfCharacters, setListOfCharacters] = useState([])
    const [listOfReaders, setListOfReaders] = useState(["serA", "serB"])
    const [newlyUploadedFiles, setNewlyUploadedFiles] = useState([])

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

    return (
        <div class="soundRegistrationPage">
            <table>
                <thead>
                    <tr>
                        <th>Character</th>
                        <th>Reader</th>
                        <th>Sound File</th>
                    </tr>
                </thead>
            </table>
            {listOfReaders.map((readerItem, readerIndex) => {
                return (<div>
                    <table>
                        <tbody>
                            {listOfCharacters.map((item, charIndex) => (
                                <tr>
                                    <td>{Object.values(item)[0]}</td>
                                    <td>{readerItem}</td>
                                    <td>
                                        <input type="file" onChange={(event) => fileUploaded(Object.values(item)[0], readerItem, event)} />
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>)
            })}

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
    )
}

export default SoundRegistration