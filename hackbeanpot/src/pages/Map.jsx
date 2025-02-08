import React, { useState } from 'react';
import useLandmark from '../hooks/useLandmark';
import Header from '../components/Header';
import Footer from '../components/Footer';

const Map = () => {
  const [city, setCity] = useState('boston'); 
  const [landmark, setLandmark] = useState('African Meeting House');
  const [searchTriggered, setSearchTriggered] = useState(false);
  const [startLocation, setStartLocation] = useState('');
  const [endLocation, setEndLocation] = useState('');
  const [tripGenerated, setTripGenerated] = useState(false);

  const { error, data: landmarkData = [] } = useLandmark(searchTriggered ? city : '', searchTriggered ? landmark : '');

  const handleLandmarkChange = (event) => {
    setLandmark(event.target.value);
  };

  const handleSearch = () => {
    if (landmark.trim() === "") {
      return;
    }
    setSearchTriggered(true);
  };

  const handleTripGeneration = () => {
    if (startLocation.trim() === "" || endLocation.trim() === "") {
      return;
    }
    // Placeholder for future MongoDB historical route query
    setTripGenerated(true);
  };

  if (error) {
    console.log('Error fetching data: ', error);
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="container my-5 flex-grow">
        <div className="mb-5 text-center">
          <h1 className="text-3xl font-bold">Historical Landmarks & Tours</h1>
          <p className="text-gray-600">Discover the rich history of your journey.</p>
        </div>

        <div className="flex flex-col md:flex-row gap-4 mb-5 justify-center">
          <input
            type="text"
            placeholder="Start Location"
            className="bg-white border rounded-[1vw] p-2 w-full md:w-1/4"
            value={startLocation}
            onChange={(e) => setStartLocation(e.target.value)}
          />
          <input
            type="text"
            placeholder="End Location"
            className="bg-white border rounded-[1vw] p-2 w-full md:w-1/4"
            value={endLocation}
            onChange={(e) => setEndLocation(e.target.value)}
          />
          <button className="bg-blue-500 text-white px-4 py-2 rounded-[1vw]" onClick={handleTripGeneration}>
            Generate Trip
          </button>
        </div>

        {tripGenerated && (
          <div className="bg-gray-100 p-4 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold">Suggested Historical Route</h2>
            <p className="text-gray-600">(Landmarks along your trip will appear here when the database is ready.)</p>
          </div>
        )}

        <div className="flex justify-center mb-5">
          <div className="flex border rounded overflow-hidden w-full md:w-1/2">
            <input
              type="text"
              placeholder="Enter landmark name..."
              className="p-2 flex-grow"
              value={landmark}
              onChange={handleLandmarkChange}
            />
            <button className="bg-blue-500 text-white px-4" onClick={handleSearch}>
              Search
            </button>
          </div>
        </div>

        {landmarkData.length > 0 && (
          <div className="max-w-lg mx-auto bg-white shadow-md rounded-lg p-5">
            <h2 className="text-xl font-bold mb-2">{landmarkData[0].Date}</h2>
            <p className="text-gray-700 mb-2">{landmarkData[0].Description}</p>
            <p className="text-gray-600 mt-2">📍 Address:&nbsp;
              <a
                href={`https://www.google.com/maps/place/${landmarkData[0].address.replace(/\s/g, '+')}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 transition duration-300"
              >
                {landmarkData[0].address}
              </a>
            </p>
            <p className="text-gray-600 mt-2">🌍 Coordinates: {landmarkData[0].lat_lon}</p>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default Map;
