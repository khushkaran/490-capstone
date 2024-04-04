import React, { useEffect, useState } from 'react'

function App() {

  const [data, setData] = useState("")

  useEffect(() => {
    console.log("inside handleGetJson");
    fetch("http://127.0.0.1:5000/members")
      .then(function (response) {
        return response.json();
      }
      )
      .then(function (myJson) {
        console.log(myJson['data'])
        setData(myJson['data'])
      })
  }, [])

  return (
    <div>
      <p>{data}</p>

    </div>
  )
}

export default App
