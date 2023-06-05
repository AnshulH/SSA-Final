import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login';
import WeatherPage from './Weather';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Login />}/>
        <Route path="/weatherdata" element={<WeatherPage />} />
      </Routes>
    </Router>
  );
};

export default App;