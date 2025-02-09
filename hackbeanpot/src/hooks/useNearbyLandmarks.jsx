import { useQuery } from '@tanstack/react-query';

const useNearbyLandmarks = (start, end, city, enabled = false) => {
  return useQuery({
    queryKey: ['nearbyLandmarks', start, end, city],
    queryFn: async () => {
      const response = await fetch(`http://127.0.0.1:5000/landmarks_nearby?city=${city}&start=${start}&end=${end}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    },
    enabled: enabled, // you might want to enable fetching only when you have valid start/end coords
  });
};

export default useNearbyLandmarks;
