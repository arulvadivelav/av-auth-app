const BASE_URL = "http://127.0.0.1:8000/v1/"

export const apiRequest = async (endpoint, method = "GET", body = null) => {
  const config = {
    method,
    headers: {
      "Content-Type": "application/json",
    }
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, config)
  const data = await response.json();

  return data;
};
