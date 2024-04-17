import React, { useEffect, useState } from 'react'

function App() {

  const [listOfCharacters, setListOfCharacters] = useState([])
  const [characterAwaitingName, setCharacterAwaitingName] = useState([])
  const [displayForm, setDisplayForm] = useState(0)

  function submitCharacterName() {
    const charName = document.forms["setCharacterNameForm"]["name"].value
    console.log(`submitCharacterName: Form has been submitted with name ${charName}, and will be associated with tag ${characterAwaitingName['tag']} and reader ${characterAwaitingName['reader']}`)

    fetch(`http://127.0.0.1:5000/addChar`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({"name": charName, "tag": characterAwaitingName['tag'], "reader": characterAwaitingName['reader']})
    }).then(function (response) {
      if (!response.ok) {
        console.log(`There is an issue with the character name.`)
      }
    }).catch(error => {
        console.log(error)
    })

    setDisplayForm(0)
    setCharacterAwaitingName([])
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

    return () => clearInterval(checkForNewCharInterval)
  }, [characterAwaitingName])

  return (
    <div class="characterRegistrationPage">
      <div class="listOfExistingCharacters">
        <table>
          <tr key="header">
            Registered Characters
          </tr>
          <tr key={"headerExplanation"}>
            The following characters have already been registered:
          </tr>
          {listOfCharacters.map((item) => (
          <tr key={item.id} class="characterName">
            {Object.values(item).map((val) => (
              <td>{val}</td>
            ))}
          </tr>
        ))}
        </table>
      </div>
      <div class="characterRegistration">
        {displayForm ? (<p>Tag detected. Give this tag a character name.</p>) : (<p>Scan a tag, and a prompt will appear to name the character associated with that tag.</p>)}
        {displayForm ? (<div class="characterRegistrationPopup">
          <form name="setCharacterNameForm" action={submitCharacterName}>
            <input name="name"/>
            <button type="button" onClick={submitCharacterName}>Submit Name</button>
          </form>
        </div>) : null}
      </div>
    </div>
  )
}

export default App
