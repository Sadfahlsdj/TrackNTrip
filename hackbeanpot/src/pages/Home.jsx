import React from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Squares from '../blocks/Squares';

const Home = () => {
  return (
    <div className="bg-black relative flex flex-col min-h-screen overflow-hidden">
      <div className="absolute inset-0 z-0">
        <Squares 
          speed={0.5} 
          squareSize={40}
          direction='diagonal'
          borderColor='rgba(94, 94, 94, 0.69)'
          hoverFillColor='#000'
        />
      </div>
      <Header />
      <main className="relative z-10 flex-grow flex flex-col items-center justify-center">
        <h1 className="text-4xl font-bold text-white">Plan Your Road Trip</h1>
        <p className="mt-4 text-lg text-white">Explore historical sites and track your carbon footprint.</p>
        <Link to="/map" className="mt-6 px-4 py-2 bg-white text-black rounded hover:bg-gray-100 transition duration-300">
          Start Planning
        </Link>
      </main>
      
      <Footer />
    </div>
  );
};

export default Home;
