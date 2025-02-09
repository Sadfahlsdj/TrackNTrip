import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { UserProvider } from './context/UserContext';
import Home from './pages/Home';
import Map from './pages/Map';
import Dashboard from './pages/Dashboard';
import NotFound from './pages/NotFound';
// import Login from './pages/Login';

const App = () => {
  return (
    <UserProvider>
      <Router>
        <div className="min-h-screen w-full">
          <Routes>
            <Route path="/" element={<Home />} />
            {/* <Route path="/login" element={<Login />} /> */}
            <Route path="/map" element={<Map />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </Router>
    </UserProvider>
  );
};

export default App;