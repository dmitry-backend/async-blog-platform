import { login, register } from './auth.js';
import { fetchPosts, fetchPostById } from './posts.js';

export const api = {
  login,
  register,
  fetchPosts,
  fetchPostById,
};
