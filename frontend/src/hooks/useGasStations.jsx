import { useQuery } from '@tanstack/react-query';

const useGasStations = (startCoords, endCoords, city = 'boston', type = 'gas') => {
  return useQuery({
    queryKey: ['gasStationData', startCoords, endCoords, type],
    queryFn: async () => {
      if (!startCoords || !endCoords) return [];
      const response = await fetch(
        `http://127.0.0.1:5000/stations?city=${city}&type=${type}&start=${startCoords.join(';')}&end=${endCoords.join(';')}`
      );
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      return data;
    },
    enabled: !!startCoords && !!endCoords,
  });
};

export default useGasStations;
