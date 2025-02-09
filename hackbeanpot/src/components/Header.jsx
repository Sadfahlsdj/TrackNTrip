import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="bg-gray-600/30 p-4 shadow-lg relative w-full">
      <div className="py-1 max-w-7xl mx-auto flex justify-between items-center">
        <Link to="/" className="text-4xl font-bold transition duration-300">TrackNTrip</Link>
        <nav>
          <ul className="flex space-x-4">
            <li>
              <Link to="/map" className="text-white transition duration-300">Map</Link>
            </li>
            <li>
              <Link to="/dashboard" className="text-white transition duration-300">Dashboard</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;