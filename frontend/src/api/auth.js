import { apiRequest } from './apiClient.js';

export const login = async ({ email, password }) => {
  const data = await apiRequest("/users/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  return {
    success: true,
    data: data
  };
};

export const register = async ({ email, password }) => {
  const data = await apiRequest("/users/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  return {
    success: true,
    data
  };
};
