import Papa from 'papaparse';
import React, { useState } from 'react';
// import characterCSV from '../../../sound_associations.csv';

function SoundPage() {
  const [parsedData, setParsedData] = useState([]);
  const [tableRows, setTableRows] = useState([]);
  const [values, setValues] = useState([]);
  const [text, setText]  = useState(null)

  //const csvFile = fs.readFileSync('../../../sound_associations.csv', 'utf8');

  Papa.parse('../../../sound_associations.csv', {
    header: true,
    download: true,
    skipEmptyLines: true,
    complete: function (results) {
      //console.log(results.data)
      const rowsArray = [];
        const valuesArray = [];

        // Iterating data to get column name and their values
        results.data.map((d) => {
          rowsArray.push(Object.keys(d));
          valuesArray.push(Object.values(d));
        });

        // Parsed Data Response in array format
        setParsedData(results.data);

        // Filtered Column Names
        setTableRows(rowsArray[0]);

        // Filtered Values
        setValues(valuesArray);
      },
    })

    const changeHandler = (event) => {
      console.log(event.target.files[0])
      Papa.parse(event.target.files[0], {
        header: true,
        skipEmptyLines: true,
        complete: function (results) {
          console.log(results.data)
        },
      });
    };


  // const changeHandler = (event) => {
  //   // Passing file data (event.target.files[0]) to parse using Papa.parse
    
  // };
  return (
   
    <div className="Sound">
      <input
        type="file"
        name="file"
        accept=".csv"
        onChange={changeHandler}
        style={{ display: "block", margin: "10px auto" }}
      />
      <header className="Sound-header">
      <p>Here is a list of your registered characters. Please choose the sound file for each reader to play for your character.
        If you don't want to play a sound file for a reader, simply leave the row blank. Press the save button when you are finished.
      </p>
      <table>
        <thead>
          <tr>
            {tableRows.map((rows, index) => {
              return <th key={index}>{rows}</th>;
            })}
          </tr>
        </thead>
        <tbody>
          {values.map((value, index) => {
            return (
              <tr key={index}>
                {value.map((val, i) => {
                  return <td key={i}>{val}</td>;
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
      {/* <table>
        <tr>
            <th>Character Name</th>
            <th>Reader</th>
            <th>Sound File</th>
        </tr>
        <tr>
            <td>Anom</td>
            <td>19</td>
            <td>Male</td>
        </tr>
        <tr>
            <td>Megha</td>
            <td>19</td>
            <td>Female</td>
        </tr>
        <tr>
            <td>Subham</td>
            <td>25</td>
            <td>Male</td>
        </tr>
    </table> */}
    </header>
    
    </div>
  );
}

export default SoundPage;
