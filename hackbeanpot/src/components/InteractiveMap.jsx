import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import angrybirdIcon from '../assets/angrybird-red.png';

const customIcon = L.icon({
  iconUrl: angrybirdIcon,
  iconSize: [38, 38],
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


const InteractiveMap = ({ landmarks, isBrainrotMode, startCoords, endCoords }) => {
  if (!landmarks || landmarks.length === 0) {
    return <div className="text-center"></div>;
  }

  const parseLatLon = (latLonStr) => {
    const [lat, lon] = latLonStr.split(';').map(Number);
    return [lat, -1 * lon];
  };

  const centerPosition = [
    landmarks.reduce((sum, landmark) => sum + parseLatLon(landmark.lat_lon)[0], 0) /
      landmarks.length,
    landmarks.reduce((sum, landmark) => sum + parseLatLon(landmark.lat_lon)[1], 0) /
      landmarks.length,
  ];

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

        {/* Render a marker for each landmark */}
        {landmarks.map((landmark, index) => {
          const position = parseLatLon(landmark.lat_lon);
          return (
            <Marker
              key={index}
              position={position}
              icon={isBrainrotMode ? customIcon : redIcon}
            >
              <Popup>
                <strong>{landmark.address}</strong>
                <br />
                {landmark.Description}
              </Popup>
            </Marker>
          );
        })}

        {/* Render the start coordinate marker if available */}
        {startCoords && (
          <Marker position={startCoords} icon={blueIcon}>
            <Popup>Start Location</Popup>
          </Marker>
        )}

        {/* Render the end coordinate marker if available */}
        {endCoords && (
          <Marker position={endCoords} icon={blueIcon}>
            <Popup>End Location</Popup>
          </Marker>
        )}
      </MapContainer>
    </div>
  );
};

export default InteractiveMap;
