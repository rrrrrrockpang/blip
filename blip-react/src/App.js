import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/Homepage'; // Adjust the import path according to your file structure
import Blip from './Blip'; // Assuming your current App component's content is moved to AppInterface

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} exact />
        <Route path="/blipdemo" element={<Blip />} />
      </Routes>
    </Router>
  );
};

export default App;
