import React from 'react';

const SavedTrips = ({ trips }) => {
  if (trips.length === 0) {
    return (
      <div></div>
    );
  }

  return (
    <div className="max-w-lg mx-auto bg-white shadow-md rounded-lg p-5">
      <h2 className="text-xl font-bold mb-4">Saved Trips</h2>
      <ul>
        {trips.map((trip, index) => (
          <li key={index} className="mb-3">
            <p className="text-gray-700">
              <strong>Trip {index + 1}:</strong> {trip.startLocation} to {trip.endLocation}
            </p>
            <p className="text-gray-500 text-sm">Date: {trip.date}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SavedTrips;
