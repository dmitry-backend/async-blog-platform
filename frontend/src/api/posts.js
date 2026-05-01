import { apiRequest } from "./apiClient";

export const fetchPosts = async ({ page = 1, size = 10 }) => {
  const data = await apiRequest(`/posts/?page=${page}&size=${size}`);   // ← added / after posts
  return {
    success: true,
    error: null,
    data,
  };
};

export const fetchPostById = async (id) => {
  const data = await apiRequest(`/posts/${id}`);
  return {
    success: true,
    error: null,
    data,
  };
};
