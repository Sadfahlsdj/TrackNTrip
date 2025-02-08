import { useQuery } from '@tanstack/react-query';
const useLandmark = (city, landmark) => {
  return useQuery({
    queryKey: ['landmarkData', city, landmark],
    queryFn: async () => {
      const response = await fetch(`http://127.0.0.1:5000/info?city=${city}&landmark=${landmark}`);

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const text = await response.text();

      try {
        const parsedData = JSON.parse(text);
        if (typeof parsedData === 'string') {
          console.log('Double-stringified detected! Parsing again...');
          let data = JSON.parse(parsedData);
          console.log(data)
          return data;
        }
        return parsedData;
      } catch (error) {
        console.error('JSON Parsing Error:', error);
        return [];
      }
    },
    enabled: !!city && !!landmark,
  });
};

export default useLandmark;