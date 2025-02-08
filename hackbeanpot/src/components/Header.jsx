import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="bg-black/20 p-4 shadow-lg fixed w-full">
      <div className="py-1 max-w-7xl mx-auto flex justify-between items-center">
        <div className="text-4xl font-bold">Road Trip Planner</div>
        <nav>
          <ul className="flex space-x-4">
            <li>
              <Link to="/" className="hover:underline">Home</Link>
            </li>
            <li>
              <Link to="/map" className="hover:underline">Map</Link>
            </li>
            <li>
              <Link to="/dashboard" className="hover:underline">Dashboard</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;