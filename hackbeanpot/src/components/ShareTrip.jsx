// src/components/ShareTrip.jsx
import React from 'react';
import { FacebookShareButton, TwitterShareButton, LinkedinShareButton, FacebookIcon, TwitterIcon, LinkedinIcon } from 'react-share';

const ShareTrip = ({ tripDetails }) => {
  const shareUrl = 'http://trackntrip.com';
  const title = `Check out my trip: ${tripDetails}`;

  return (
    <div className="mt-10">
      <h3 className="text-2xl font-semibold text-center mb-4">Share Your Trip</h3>
      <div className="flex justify-center space-x-4 mb-4">
        <FacebookShareButton url={shareUrl} quote={title}>
          <FacebookIcon size={32} round />
        </FacebookShareButton>
        <TwitterShareButton url={shareUrl} title={title}>
          <TwitterIcon size={32} round />
        </TwitterShareButton>
        <LinkedinShareButton url={shareUrl} title={title}>
          <LinkedinIcon size={32} round />
        </LinkedinShareButton>
      </div>
    </div>
  );
};

export default ShareTrip;
