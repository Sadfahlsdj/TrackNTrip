
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend } from 'recharts';
import Header from '../components/Header';
import Footer from '../components/Footer';
import ShareTrip from '../components/ShareTrip';
import Gamification from '../components/Gamification';

const Dashboard = () => {
  const [totalEmissions, setTotalEmissions] = useState(0);
  const [averageEmissions, setAverageEmissions] = useState(0);
  const [tripCount, setTripCount] = useState(0);
  const [badges, setBadges] = useState([]);
  const [streaks, setStreaks] = useState({ current: 0, longest: 0 });

  const emissionsData = [
    { name: 'Car', value: 400 },
    { name: 'Bus', value: 300 },
    { name: 'Train', value: 200 },
    { name: 'Airplane', value: 100 },
  ];

  const emissionsOverTime = [
    { month: 'Jan', emissions: 200 },
    { month: 'Feb', emissions: 300 },
    { month: 'Mar', emissions: 250 },
    { month: 'Apr', emissions: 400 },
    { month: 'May', emissions: 350 },
  ];

  useEffect(() => {
    const fetchData = () => {
      const totalEmissions = 200;
      const averageEmissions = 100;
      const tripCount = 6;

      setTotalEmissions(totalEmissions);
      setAverageEmissions(averageEmissions);
      setTripCount(tripCount);

      const earnedBadges = [];

      if (totalEmissions <= 1000) {
        earnedBadges.push({ name: 'Eco Warrior', description: 'Kept total emissions below 1000 kg CO2', icon: '🌍' });
      }

      if (averageEmissions <= 250) {
        earnedBadges.push({ name: 'Efficient Traveler', description: 'Maintained average emissions below 250 kg CO2 per trip', icon: '🚴' });
      }

      if (tripCount >= 5) {
        earnedBadges.push({ name: 'Frequent Traveler', description: 'Completed 5 or more trips', icon: '✈️' });
      }

      setBadges(earnedBadges);
      setStreaks({ current: 5, longest: 10 });
    };

    fetchData();
  }, []);

  return (
    <>
      <Header />
      <div className="px-10 py-6 w-full">
        <h2 className="py-5 text-5xl font-bold text-center">Carbon Footprint Dashboard</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          <motion.div
            className="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <h3 className="text-lg font-semibold">Total Emissions (kg CO2)</h3>
            <motion.div
              className="text-4xl font-bold text-green-800"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1 }}
            >
              {totalEmissions}
            </motion.div>
          </motion.div>

          <motion.div
            className="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <h3 className="text-lg font-semibold">Average Emissions per Trip (kg CO2)</h3>
            <motion.div
              className="text-4xl font-bold text-green-800"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1 }}
            >
              {averageEmissions}
            </motion.div>
          </motion.div>

          <motion.div
            className="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <h3 className="text-lg font-semibold">Total Trips</h3>
            <motion.div
              className="text-4xl font-bold text-green-800"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1 }}
            >
              {tripCount}
            </motion.div>
          </motion.div>
        </div>

        <div className="mt-10">
          <h3 className="text-2xl font-semibold text-center">Emissions Breakdown by Transportation Type</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={emissionsData}
                cx="50%"
                cy="40%"
                labelLine={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {emissionsData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={['#0088FE', '#00C49F', '#FFBB28', '#FF8042'][index % 4]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-10">
          <h3 className="text-2xl font-semibold text-center">Emissions Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={emissionsOverTime}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="emissions" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <Gamification badges={badges} streaks={streaks} />

        <ShareTrip tripDetails={`Total Emissions: ${totalEmissions} kg CO2, Average Emissions per Trip: ${averageEmissions} kg CO2, Total Trips: ${tripCount}`} />
      </div>
      <Footer />
    </>
  );
};

export default Dashboard;
