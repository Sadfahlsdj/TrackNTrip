import React, { createContext, useState, useEffect } from 'react';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('user');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const [savedTrips, setSavedTrips] = useState(() => {
    const trips = localStorage.getItem('savedTrips');
    return trips ? JSON.parse(trips) : [];
  });

  useEffect(() => {
    localStorage.setItem('user', JSON.stringify(user));
  }, [user]);

  useEffect(() => {
    localStorage.setItem('savedTrips', JSON.stringify(savedTrips));
  }, [savedTrips]);

  return (
    <UserContext.Provider value={{ user, setUser, savedTrips, setSavedTrips }}>
      {children}
    </UserContext.Provider>
  );
};
