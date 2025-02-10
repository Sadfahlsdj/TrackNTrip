import React from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Squares from '../blocks/Squares';

const Home = () => {
  return (
    <div className="bg-beige relative flex flex-col min-h-screen overflow-hidden">
      <div className="absolute inset-0 z-0">
        <Squares 
          speed={0.5} 
          squareSize={40}
          direction='diagonal'
          borderColor='#a4ba8d'
          hoverFillColor='#000'
        />
      </div>
      <Header />
      <main className="relative z-10 flex-grow flex flex-col items-center justify-center">
        <h1 className="text-4xl font-bold text-brown drop-shadow-lg">TrackNTrip</h1>
        <p className="mt-4 text-lg text-brown font-semibold drop-shadow-sm">
            Explore historical sites and track your carbon footprint.
          </p>
        <Link to="/map" className="mt-6 px-4 py-2 bg-greenRT text-white rounded hover:bg-gray-100 transition duration-300 drop-shadow-sm">
          Start Planning
        </Link>
      </main>
      
      <Footer />
    </div>
  );
};

export default Home;
