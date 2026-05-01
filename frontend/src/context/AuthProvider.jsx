import React, { useState } from "react";
import { AuthContext } from "./AuthContext";
import { api } from "../api";

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem("user");
    return storedUser ? JSON.parse(storedUser) : null;
  });

  const loginUser = async (credentials) => {
    const response = await api.login(credentials);

    // Safety check
    if (!response?.success || !response?.data?.access_token) {
      throw new Error("Invalid login response");
    }

    const token = response.data.access_token;

    let payload;
    try {
      // Handle real JWT
      const payloadPart = token.split('.')[1];
      if (!payloadPart) throw new Error("Invalid token format");
      payload = JSON.parse(atob(payloadPart));
    } catch (e) {
      // Fallback for mock token
      payload = { sub: "1", role: "user" };
    }

    const userData = {
      id: parseInt(payload.sub || 1),
      email: credentials.email,
      role: payload.role || "user",
      token: token,
    };

    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData));

    return userData;
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  return (
    <AuthContext.Provider value={{ user, loading: false, login: loginUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
