import React, { useState } from 'react';
import useLandmark from '../hooks/useLandmark';
import useCoords from '../hooks/useCoords';
import useGasStations from '../hooks/useGasStations';
import Header from '../components/Header';
import Footer from '../components/Footer';
import SavedTrips from '../components/SavedTrips';
import InteractiveMap from '../components/InteractiveMap';
import bombIcon from '../assets/angrybird-bomb.png';

const Map = ({ initialCity = 'boston' }) => {
  const [city, setCity] = useState(initialCity);
  const [landmark, setLandmark] = useState('');
  const [searchTriggered, setSearchTriggered] = useState(false);
  const [startLocation, setStartLocation] = useState('');
  const [endLocation, setEndLocation] = useState('');
  const [vehicleType, setVehicleType] = useState('gas');
  const [tripGenerated, setTripGenerated] = useState(false);
  const [savedTrips, setSavedTrips] = useState([]);
  const [isBrainrotMode, setIsBrainrotMode] = useState(false);

  const { error, data: landmarkData = [] } = useLandmark(
    searchTriggered ? city : '',
    searchTriggered ? landmark : ''
  );

  const handleLandmarkChange = (event) => {
    setLandmark(event.target.value);
  };

  const handleSearch = () => {
    if (landmark.trim() === '') {
      return;
    }
    setSearchTriggered(true);
  };

  const {
    data: startCoords,
    refetch: refetchStartCoords,
    isFetching: isFetchingStartCoords,
  } = useCoords(startLocation, { enabled: false });

  const {
    data: endCoords,
    refetch: refetchEndCoords,
    isFetching: isFetchingEndCoords,
  } = useCoords(endLocation, { enabled: false });

  const handleTripGeneration = async () => {
    if (startLocation.trim() === '' || endLocation.trim() === '') {
      return;
    }
    try {
      await Promise.all([refetchStartCoords(), refetchEndCoords()]);
      setTripGenerated(true);
    } catch (error) {
      console.error('Error fetching coordinates:', error);
    }
  };

  const handleSaveTrip = () => {
    if (startLocation && endLocation) {
      const newTrip = {
        startLocation,
        endLocation,
        date: new Date().toLocaleDateString(),
      };
      setSavedTrips([...savedTrips, newTrip]);
      setStartLocation('');
      setEndLocation('');
      setTripGenerated(false);
    }
  };

  const toggleBrainrotMode = () => {
    setIsBrainrotMode(!isBrainrotMode);
  };

  const { data: gasStations } = useGasStations(startCoords, endCoords, city, vehicleType);


  if (error) {
    console.log('Error fetching data: ', error);
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="container mx-auto my-5 flex-grow">
        <div className="mb-5 text-center">
          <h1 className="pt-5 pb-3 text-3xl font-bold">
            Explore Your Route
          </h1>
          <p className="text-gray-600">
            Discover historic landmarks and fuel savings along your route.
          </p>
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
          <select
            className="bg-white border rounded-[1vw] p-2 w-full md:w-1/8"
            value={vehicleType}
            onChange={(e) => setVehicleType(e.target.value)}
          >
            <option value="gas">Gas Vehicle</option>
            <option value="electric">Electric Vehicle</option>
          </select>
          <button
            className="px-4 py-3 bg-gray-500 text-white rounded-[1vw] hover:bg-gray-600 transition duration-300"
            onClick={handleTripGeneration}
            disabled={isFetchingStartCoords || isFetchingEndCoords}
          >
            {isFetchingStartCoords || isFetchingEndCoords
              ? 'Generating...'
              : 'Generate Trip'}
          </button>
        </div>
        {tripGenerated && (
          <div className="flex flex-col justify-center bg-gray-100 p-4 w-90 rounded-lg shadow-md mb-5 mx-auto">
            <h2 className="text-xl font-semibold">Suggested Historical Route</h2>
            <p className="text-gray-600">
              (Landmarks along your trip will appear here when the database is ready.)
            </p>
            <button
              className="mt-3 bg-greenRT text-white py-2 px-4 rounded-[1vw]"
              onClick={handleSaveTrip}
            >
              Save Trip
            </button>
          </div>
        )}



        <div className="flex justify-center">
          <div className="flex border bg-white rounded-[1vw] overflow-hidden w-full md:w-1/2">
            <input
              type="text"
              placeholder="Enter landmark name..."
              className="p-2 flex-grow"
              value={landmark}
              onChange={handleLandmarkChange}
            />
            <button
              className="px-4 py-3 bg-gray-500 text-white hover:bg-gray-600 transition duration-300"
              onClick={handleSearch}
            >
              Search
            </button>
          </div>

          <button className="ml-6" onClick={toggleBrainrotMode}>
            <img src={bombIcon} alt="Toggle TNT Mode" className="h-9 w-9" />
          </button>
        </div>

        <InteractiveMap
          landmarks={landmarkData}
          isBrainrotMode={isBrainrotMode}
          startCoords={startCoords}
          endCoords={endCoords}
          gasStations={gasStations}
        />

        <div className="flex flex-col md:flex-row gap-4 mt-3">
          {gasStations && gasStations.length > 0 && (
            <div className="flex-1 bg-white shadow-md rounded-lg p-5 mb-5">
              <h2 className="text-xl font-bold mb-4">Gas Stations</h2>
              <ul>
                {gasStations.map((station, index) => (
                  <li key={`gas-station-${index}`} className="mb-4 border-b pb-2">
                    <h3 className="text-lg font-semibold mb-2">
                      {index + 1}. {station.name}
                    </h3>
                    <p className="text-gray-600">Address: {station.address}</p>
                    <p className="text-gray-600">
                      Price per Gallon: ${station.price_per_gallon.toFixed(2)}
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {landmarkData.length > 0 && (
            <div className="flex-1 bg-white shadow-md rounded-lg p-5 mb-5">
              <h2 className="text-xl font-bold mb-4">Landmarks</h2>
              <p className="font-semibold text-lg mb-2">{landmarkData[0].Date}</p>
              <p className="text-gray-700 mb-2">
                {landmarkData[0].Description}
              </p>
              <p className="text-gray-600 mt-2">
                📍 Address:&nbsp;
                <a
                  href={`https://www.google.com/maps/place/${landmarkData[0].address.replace(
                    /\s/g,
                    '+'
                  )}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 transition duration-300"
                >
                  {landmarkData[0].address}
                </a>
              </p>
              <p className="text-gray-600 mt-2">
                🌍 Coordinates: {landmarkData[0].lat_lon}
              </p>
            </div>
          )}
        </div>

        <SavedTrips trips={savedTrips} />
      </div>
      <Footer />
    </div>
  );
};

export default Map;
