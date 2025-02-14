import { useQuery } from '@tanstack/react-query';

const useNearbyLandmarks = (start, end, city) => {
  return useQuery({
    queryKey: ['nearbyLandmarks', start, end, city],
    queryFn: async () => {
      if (!start || !end) return [];
      const response = await fetch(`http://127.0.0.1:5000/landmarks?start=${start.join(';')}&end=${end.join(';')}&city=${city}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    },
    enabled: !!start && !!end,
  });
};

export default useNearbyLandmarks;
