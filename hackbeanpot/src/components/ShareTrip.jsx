// src/components/ShareTrip.jsx
import React from 'react';
import { FacebookShareButton, TwitterShareButton } from 'react-share';

const ShareTrip = ({ tripDetails }) => {
  const shareUrl = 'http://yourwebsite.com'; // Replace with your website URL
  const title = `Check out my trip: ${tripDetails}`;

  return (
    <div>
      <h2 className="text-2xl font-bold">Share Your Trip</h2>
      <FacebookShareButton url={shareUrl} quote={title}>
        Share on Facebook
      </FacebookShareButton>
      <TwitterShareButton url={shareUrl} title={title}>
        Share on Twitter
      </TwitterShareButton>
    </div>
  );
};

export default ShareTrip;