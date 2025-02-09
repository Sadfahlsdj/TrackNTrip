import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import angrybirdRedIcon from '../assets/angrybird-red.png';
import angrybirdBlueIcon from '../assets/angrybird-blue.png';
import angrybirdGreenIcon from '../assets/angrybird-green.png';

const redBirdIcon = L.icon({
  iconUrl: angrybirdRedIcon,
  iconSize: [38, 38],
  iconAnchor: [19, 38],
  popupAnchor: [0, -38],
});

const blueBirdIcon = L.icon({
  iconUrl: angrybirdBlueIcon,
  iconSize: [38, 38],
  iconAnchor: [19, 38],
  popupAnchor: [0, -38],
});

const greenBirdIcon = L.icon({
  iconUrl: angrybirdGreenIcon,
  iconSize: [48, 38],
  iconAnchor: [19, 38],
  popupAnchor: [0, -38],
});


const blueIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
  shadowSize: [41, 41],
});

const redIcon = L.icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
  shadowSize: [41, 41],
});

const greenIcon = L.icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
  shadowSize: [41, 41],
});

const InteractiveMap = ({
  landmarks,
  isBrainrotMode,
  startCoords,
  endCoords,
  gasStations,
}) => {
  if (!landmarks || landmarks.length === 0) {
    return <div className="text-center"></div>;
  }

  const parseLatLon = (latLonInput) => {
    if (Array.isArray(latLonInput)) {
      return latLonInput;
    } else if (typeof latLonInput === 'string') {
      const parts = latLonInput.split(';').map(Number);
      if (parts.length < 2 || isNaN(parts[0]) || isNaN(parts[1])) return null;
      return [parts[0], -parts[1]];
    }
    return null;
  };

  const validLandmarkPositions = landmarks
    .map((landmark) => parseLatLon(landmark.lat_lon))
    .filter((pos) => pos !== null);

  const centerPosition =
    validLandmarkPositions.length > 0
      ? [
          validLandmarkPositions.reduce((sum, pos) => sum + pos[0], 0) /
            validLandmarkPositions.length,
          validLandmarkPositions.reduce((sum, pos) => sum + pos[1], 0) /
            validLandmarkPositions.length,
        ]
      : [0, 0];

  return (
    <div className="flex justify-center items-center h-screen">
      <MapContainer
        center={centerPosition}
        zoom={13}
        className="h-[80%] w-[90%] border rounded-[1vw]"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {landmarks.map((landmark, index) => {
          const position = parseLatLon(landmark.lat_lon);
          if (!position) return null;
          return (
            <Marker
              key={`landmark-${index}`}
              position={position}
              icon={isBrainrotMode ? redBirdIcon : redIcon}
            >
              <Popup>
                <strong>{landmark.address}</strong>
                <br />
                {landmark.Description}
              </Popup>
            </Marker>
          );
        })}

        {startCoords && (
          <Marker 
            position={startCoords} 
            icon={isBrainrotMode ? blueBirdIcon : blueIcon}>
            <Popup>Start Location</Popup>
          </Marker>
        )}

        {endCoords && (
          <Marker 
            position={endCoords} 
            icon={isBrainrotMode ? blueBirdIcon : blueIcon}>
            <Popup>End Location</Popup>
          </Marker>
        )}

        {gasStations &&
          gasStations.length > 0 &&
          gasStations.map((station, index) => {
            const position = parseLatLon(station.latlons);
            if (!position) return null;
            return (
              <Marker key={`gas-${index}`} position={position} icon={isBrainrotMode ? greenBirdIcon : greenIcon}>
                <Popup>
                  <strong>{station.name || 'Gas Station'}</strong>
                  <br />
                  {station.address}
                </Popup>
              </Marker>
            );
          })}
      </MapContainer>
    </div>
  );
};

export default InteractiveMap;

