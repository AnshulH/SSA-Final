import React, { useState } from 'react';
import axios from 'axios';
import {useNavigate } from "react-router-dom";
import './Login.css'; // Import the CSS file for styling

const Login = () => {
  const [username, setUsername] = useState('');
  const [location, setLocation] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('https://0li1jd0m9l.execute-api.us-east-2.amazonaws.com/Gamma/login/', {
        username
      });

      // Handle the API response
      if (response.data === "Username already exists") {
        console.log("welcome back");
        navigate("/weatherdata/", {state: {
            username: username,
            location: location
        }});
      } else {
        console.log("Hello");
        navigate("/weatherdata/", {state: {
            username: username,
            location: location
        }});
      }
    } catch (error) {
      // Handle errors
      console.error(error);
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Username:</label>
          <input
            className="form-input"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Location:</label>
          <input
            className="form-input"
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
        </div>
        <button className="submit-button" type="submit">Submit</button>
      </form>
    </div>
  );
};

export default Login;