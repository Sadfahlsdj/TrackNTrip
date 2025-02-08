// src/components/Home.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header.jsx';
import Footer from '../components/Footer.jsx';


const Home = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow flex flex-col items-center justify-center pt-16"> {/* Added padding-top to avoid overlap */}
        <h1 className="text-4xl font-bold">Plan Your Road Trip</h1>
        <p className="mt-4 text-lg">Explore historical sites and track your carbon footprint.</p>
        <Link to="/map" className="mt-6 px-4 py-2 bg-white text-green rounded hover:bg-gray-100 transition duration-300">
          Start Planning
        </Link>
      </main>

      <Footer />
    </div>
  );
};

export default Home;