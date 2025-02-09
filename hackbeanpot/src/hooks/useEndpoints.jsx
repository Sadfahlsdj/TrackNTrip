import { useQuery } from '@tanstack/react-query';

const useEndpoints = (coords) => {
  return useQuery({
    queryKey: ['endpointData', coords],
    queryFn: async () => {
      const response = await fetch(`http://127.0.0.1:5000/info?city=boston&landmark=${coords}`);

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      return data;
    },
    enabled: !!coords,
  });
};

export default useEndpoints;