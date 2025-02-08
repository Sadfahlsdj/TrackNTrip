// src/components/UserPreferences.jsx
import React, { useState } from 'react';

const UserPreferences = () => {
  const [preferences, setPreferences] = useState({
    distance: '',
    cost: '',
    mustVisit: '',
  });

  const handleChange = (e) => {
    setPreferences({ ...preferences, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission, e.g., save preferences to the database
    console.log(preferences);
  };

  return (
    <form onSubmit={handleSubmit} className="p-4">
      <h2 className="text-2xl font-bold">Input Your Preferences</h2>
      <div>
        <label>Max Distance:</label>
        <input type="text" name="distance" onChange={handleChange} />
      </div>
      <div>
        <label>Max Cost:</label>
        <input type="text" name="cost" onChange={handleChange} />
      </div>
      <div>
        <label>Must Visit Places:</label>
        <input type="text" name="mustVisit" onChange={handleChange} />
      </div>
      <button type="submit" className="mt-4 bg-blue-500 text-white p-2 rounded">Submit</button>
    </form>
  );
};

export default UserPreferences;