'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authApi';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null);

  useEffect(() => {
    // Check if there's a token and validate it
    const initializeAuth = async () => {
      if (typeof window !== 'undefined') {
        const storedToken = localStorage.getItem('token');
        if (storedToken) {
          setToken(storedToken);

          try {
            const userData = await authService.getCurrentUser();
            setUser(userData);
          } catch (error) {
            // Token is invalid, clear it
            localStorage.removeItem('token');
            setToken(null);
            setUser(null);
          }
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const response = await authService.login(email, password);
      const { access_token } = response;

      // Store token in localStorage and state
      if (typeof window !== 'undefined') {
        localStorage.setItem('token', access_token);
      }
      setToken(access_token);

      // Get user data
      const userData = await authService.getCurrentUser();
      setUser(userData);

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.response?.data?.msg || error.response?.data?.message || error.message || 'Login failed'
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authService.register(userData);
      // After registration, log the user in
      return await login(userData.email, userData.password);
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.response?.data?.msg || error.response?.data?.message || error.message || 'Registration failed'
      };
    }
  };

  const logout = () => {
    // Remove token from localStorage and state
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
    setToken(null);
    setUser(null);
  };

  const value = {
    user,
    token,
    login,
    register,
    logout,
    isAuthenticated: !!user,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};