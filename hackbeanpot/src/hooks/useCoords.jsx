import { useQuery } from '@tanstack/react-query';

const useCoords = (address, options = {}) => {
  return useQuery({
    queryKey: ['coords', address],
    queryFn: async () => {
      const response = await fetch(
        `http://127.0.0.1:5000/coords?address=${encodeURIComponent(address)}`
      );
      console.log(response);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      
      return data.coords.split(';').map(Number);
    },

    enabled: !!address && (options.enabled !== undefined ? options.enabled : !!address),
    ...options,
  });
};

export default useCoords;
