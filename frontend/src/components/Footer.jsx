import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-brown relative bottom-0 text-white p-4 mt-auto">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <p className="text-sm">© 2025 TrackNTrip. All rights reserved.</p>
        <div className="flex space-x-4">
          <a href="https://tiktok.com" target="_blank" rel="noopener noreferrer" className="hover:underline">TikTok</a>
          <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="hover:underline">Twitter</a>
          <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="hover:underline">Instagram</a>
        </div>
      </div>
    </footer>
  )
}

export default Footer;