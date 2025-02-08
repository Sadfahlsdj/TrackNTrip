import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const InteractiveMap = ({ landmarks }) => {
  if (!landmarks || landmarks.length === 0) {
    return <div className="text-center"></div>;
  }

  const parseLatLon = (latLonStr) => {
    const [lat, lon] = latLonStr.split(';').map(Number);
    return [lat, -1 * lon];
  };

  const centerPosition = [
    landmarks.reduce((sum, landmark) => sum + parseLatLon(landmark.lat_lon)[0], 0) / landmarks.length,
    landmarks.reduce((sum, landmark) => sum + parseLatLon(landmark.lat_lon)[1], 0) / landmarks.length,
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
        {landmarks.map((landmark, index) => {
          const position = parseLatLon(landmark.lat_lon);
          return (
            <Marker key={index} position={position}>
              <Popup>
                <strong>{landmark.address}</strong><br />
                {landmark.Description}
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
};

export default InteractiveMap;
