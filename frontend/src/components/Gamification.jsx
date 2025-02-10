import React from 'react';

const Gamification = ({ badges, streaks }) => {
  return (
    <div className="mt-10 flex flex-col items-center">
      <h3 className="text-2xl font-semibold mb-6">Your Achievements</h3>
      <div className="flex justify-center space-x-4 mb-6">
        {badges.map((badge, index) => (
          <div key={index} className="bg-white shadow-lg rounded-lg p-4 flex flex-col items-center">
            <h1 className="text-5xl">{badge.icon}</h1>
            <h4 className="text-lg font-semibold">{badge.name}</h4>
            <p className="text-sm text-gray-600 text-center">{badge.description}</p>
          </div>
        ))}
      </div>
      
      <div>
        <div className="bg-white shadow-lg rounded-xl p-6 flex flex-col items-center w-82">
          <div className="relative flex items-center justify-center mb-4">
            <div className="bg-greenRT rounded-full w-20 h-20 flex items-center justify-center text-3xl font-bold text-white">
              {streaks.current}
            </div>
          </div>
          <h4 className="text-xl font-bold">Streak</h4>
          <p className="text-sm text-gray-600">Add a trip every day to build your streak</p>
          
          <div className="flex flex-col items-center mt-4">
            <div className="grid grid-cols-7 gap-2 text-center w-full">
              {['Tu', 'W', 'Th', 'F', 'Sa', 'Su', 'M'].map((day, index) => (
                <span key={index} className="text-sm font-bold text-gray-700">{day}</span>
              ))}
            </div>
            <div className="grid grid-cols-7 gap-2 mt-1">
              {['Tu', 'W', 'Th', 'F', 'Sa', 'Su', 'M'].map((day, index) => (
                <div key={index} className={`w-8 h-8 flex items-center justify-center rounded-full ${index < 6 ? 'bg-greenRT' : 'bg-gray-300'}`}>
                  <span className="text-white font-bold">✓</span>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="bg-greenRT shadow-lg rounded-xl p-6 flex flex-col items-center w-82 mt-6 text-white">
          <h4 className="text-xl font-bold">Longest Streak</h4>
          <div className="text-3xl font-bold">{streaks.longest} days</div>
        </div>
      </div>
    </div>
  );
};

export default Gamification;
