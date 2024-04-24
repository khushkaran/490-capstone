import React, { useEffect, useState } from 'react'

function CharacterRegistration() {

  const [listOfCharacters, setListOfCharacters] = useState([])
  const [characterAwaitingName, setCharacterAwaitingName] = useState([])
  const [displayForm, setDisplayForm] = useState(0)
  const [invalidCharacterForm, setInvalidCharacterForm] = useState(0)

  function submitCharacterName() {
    const charName = document.forms["setCharacterNameForm"]["name"].value
    if (charName.length < 1 || charName.length > 12) {
      setInvalidCharacterForm(1);
      console.log("Setting invalidCharacterForm to 1")
    } else {
      console.log(`submitCharacterName: Form has been submitted with name ${charName}, and will be associated with tag ${characterAwaitingName['tag']} and reader ${characterAwaitingName['reader']}`)

      fetch(`http://127.0.0.1:5000/modifyChar`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "name": charName, "tag": characterAwaitingName['tag'], "reader": characterAwaitingName['reader'] })
      }).then(function (response) {
        if (!response.ok) {
          setInvalidCharacterForm(1);
          console.log(`There is an issue with the character name.`)
        }
      }).catch(error => {
        setInvalidCharacterForm(1);
        console.log(error)
      })
    }

    setDisplayForm(0)
    setCharacterAwaitingName([])
  }

  function deleteCharacterName(charName) {
    console.log(`Trying to delete ${charName}.`)
    fetch(`http://127.0.0.1:5000/modifyChar`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "name": charName })
    }).then(function (response) {
      if (!response.ok) {
        console.log(`Character ${charName} was not deleted.`)
      } else {
        console.log('Fetching character list after deletion.')
        fetch('http://127.0.0.1:5000/getAllChar', {
          method: 'GET',
        }).then(function (response) {
          return response.json();
        }).then(function (myJson) {
          setListOfCharacters(myJson)
          console.log(`GET call to getAllChar completed, and ${listOfCharacters} stored in listOfCharacters.`)
        })
      }
    }).catch(error => {
      console.log(error)
    })    
  }

  useEffect(() => {
    fetch('http://127.0.0.1:5000/getAllChar', {
      method: 'GET',
    }).then(function (response) {
      return response.json();
    }).then(function (myJson) {
      setListOfCharacters(myJson)
      console.log(`GET call to getAllChar completed, and ${listOfCharacters} stored in listOfCharacters.`)
    })

    let checkForInvalidCharacterSubmittedInterval = setInterval(() => {
      setInvalidCharacterForm(0);
    }, 5000)

    let checkForNewCharInterval = setInterval(() => {
      fetch('http://127.0.0.1:5000/getRecentlyScannedChar', {
        method: 'GET',
      }).then(function (response) {
        return response.json();
      }).then(function (myJson) {
        const newChars = myJson
        setCharacterAwaitingName(newChars)
      })
    }, 1000)

    console.log(`GET call to getRecentlyScannedChar completed, and ${characterAwaitingName} stored in characterAwaitingName.`)
    if (Object.keys(characterAwaitingName).length !== 0) {
      if (characterAwaitingName['tag']) {
        console.log('characterAwaitingName contains a valid tag-reader combination, rendering form.')
        setDisplayForm(1)
      }
      clearInterval(checkForNewCharInterval) // To check once the arduino is hooked up: This might have to be moved in the if
      // statement that is above this. 
    } else {
      console.log('characterAwaitingName does not contain a valid tag-reader combination. Form will not be rendered.')
    }

    return () => {clearInterval(checkForNewCharInterval)
    clearInterval(checkForInvalidCharacterSubmittedInterval)}
  }, [characterAwaitingName, invalidCharacterForm])

  return (
    <div class="characterRegistrationPage">
      <div class="listOfExistingCharacters">
        <h1 key={"header"}>Register Tags and Characters</h1>
        {(Object.keys(listOfCharacters).length === 0) ? (<h3 key={"headerExplanation"}>There are currently no registered characters.</h3>) : (<h3 key={"headerExplanation"}>The following characters have already been registered:</h3>)}
        <div class="characterNamesContainer">
          {listOfCharacters.map((item) => (
            <div class="characterNameItem">
              {Object.values(item).map((val) => (
                <button class="nameButtonDelete" onClick={() => deleteCharacterName(val)}>{val}</button>
              ))}
            </div>
          ))
          }
        </div>
      </div>
      <div class="characterRegistration">
        <h3>Register New Characters:</h3>
        {displayForm ? (<p class='scanTag'>Tag detected. Give this tag a character name.</p>) : (<p class='scanTag'>Scan a tag, and a prompt will appear to name the character associated with that tag.</p>)}
        {displayForm ? (<div class="characterRegistrationPopup">
          <form class="setCharacterNameForm" name="setCharacterNameForm" action={submitCharacterName}>
            <input class="characterNameInput" name="name" />
            <button class="submitButton" type="button" onClick={submitCharacterName}>Submit Name</button>
          </form>
        {invalidCharacterForm ? (<p class="invalidCharacterSubmitted">The character name you submitted is invalid. Please ensure your character names are unique and between 1 and 12 characters in length.</p>) : null}
        </div>) : null}
      </div>
    </div>
  )
}

export default CharacterRegistration
