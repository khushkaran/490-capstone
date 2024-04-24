import { BrowserRouter as Router, Route , Routes} from 'react-router-dom';
import CharacterRegistration from './CharacterRegistration';
import SoundRegistration from './SoundRegistration';
import ReaderRegistration from './ReaderRegistration';
import './App.css';
import React from 'react';

function App() {
    return (
        <Router>
            <Routes>
                <Route path='/' element={<ReaderRegistration/>} />
                <Route path='characterRegistration' element={<CharacterRegistration/>}/>
                <Route path='soundRegistration' element={<SoundRegistration/>}/>
            </Routes>
        </Router>
    );
  }
  
  export default App;