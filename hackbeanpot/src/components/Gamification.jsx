import React from 'react';

const Gamification = ({ badges, streaks }) => {
  return (
    <div className="mt-10">
      <h3 className="text-2xl font-semibold text-center mb-4">Your Achievements</h3>
      <div className="flex justify-center space-x-4">
        {badges.map((badge, index) => (
          <div key={index} className="bg-white shadow-lg rounded-lg p-4 flex flex-col items-center">
            <h1 className="text-5xl">{badge.icon}</h1>
            <h4 className="text-lg font-semibold">{badge.name}</h4>
            <p className="text-sm text-gray-600">{badge.description}</p>
          </div>
        ))}
      </div>
      <div className="mt-3 text-center">
        <h4 className="text-lg text-gray-600 font-semibold">Current Streak: {streaks.current} days</h4>
        <h4 className="text-lg text-gray-600 font-semibold">Longest Streak: {streaks.longest} days</h4>
      </div>
    </div>
  );
};

export default Gamification;
