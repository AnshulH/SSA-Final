import React, { useState, useEffect } from 'react';
import {useLocation} from 'react-router-dom';

import './Weather.css';

const WeatherPage = () => {
  const [weatherData, setWeatherData] = useState(null);
  const location = useLocation();
//   const { username } = location.state.username;

  useEffect(() => {
    // Fetch weather data from the AWS Gateway API
    fetchWeatherData();
  }, []);

  const fetchWeatherData = async () => {
    try {
      const response = await fetch('https://0li1jd0m9l.execute-api.us-east-2.amazonaws.com/Gamma/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          location: location.state.location,
          username: location.state.username
        }),
      });
      const responseData = await response.json();
      const { body } = responseData;
      const data = JSON.parse(body);

      setWeatherData(data);
      console.log(data.location);
    } catch (error) {
      console.log('Error fetching weather data:', error);
    }
  };

  return (
    <div className="weather-container">
      {weatherData ? (
        <>
        <h1>Welcome {location.state.username}</h1>
          <h1 className="location">{weatherData.location} Weather details</h1>
          <div className="weather-info">
            <p className="temperature">
            Temperature: {Math.round(weatherData.data.temperature_fahrenheit)}°F
            </p>
            <p className="heat-index">Heat Index: {weatherData.data.heat_index}</p>
            <p className="wind-chill">Wind Chill: {weatherData.data.wind_chill}</p>
            <p className="visibility">Visibility: {weatherData.data.visibility}</p>
            <p className="humidity">Humidity: {weatherData.data.humidity}%</p>
          </div>
          <h2>Your previous location searches:</h2>
          <ul>
            {weatherData.locations.map((location, index) => (
              <li key={index}>{location}</li>
            ))}
          </ul>
        </>
      ) : (
        <p>Loading weather data...</p>
      )}
    </div>
  );
};

export default WeatherPage;
