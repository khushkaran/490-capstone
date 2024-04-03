import React, { useEffect, useState } from 'react'

function App() {

  const [data, setData] = useState([{}])

  useEffect(() => {
    console.log("inside handleGetJson");
    fetch("http://127.0.0.1:5000/members")
      .then(
        data => {
          setData(data)
          console.log(data)
        }
      )
  }, [])

  return (
    <div>


    </div>
  )
}

export default App
