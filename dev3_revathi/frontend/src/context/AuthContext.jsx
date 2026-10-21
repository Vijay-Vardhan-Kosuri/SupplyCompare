import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('supplycompare_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState(() => localStorage.getItem('supplycompare_token') || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      api.get('/auth/me/')
        .then((res) => {
          setUser(res.data.user);
          localStorage.setItem('supplycompare_user', JSON.stringify(res.data.user));
        })
        .catch(() => {
          logout();
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (email, password) => {
    const res = await api.post('/auth/login/', { email, password });
    const { user, tokens } = res.data;
    setUser(user);
    setToken(tokens.access);
    localStorage.setItem('supplycompare_token', tokens.access);
    localStorage.setItem('supplycompare_user', JSON.stringify(user));
    return user;
  };

  const register = async (userData) => {
    const res = await api.post('/auth/register/', userData);
    const { user, tokens } = res.data;
    setUser(user);
    setToken(tokens.access);
    localStorage.setItem('supplycompare_token', tokens.access);
    localStorage.setItem('supplycompare_user', JSON.stringify(user));
    return user;
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('supplycompare_token');
    localStorage.removeItem('supplycompare_user');
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
