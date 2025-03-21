import React, { useState, useEffect } from "react";
import { AuthContext } from "../contexts/AuthContext";
import axios from "axios";

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const validateToken = async () => {
    try {
      const response = await axios.get("api/auth/validate", {
        withCredentials: true,
      });
      if (response.data.autenticado) {
        setUser(response.data.usuario);
      } else {
        setUser(null);
      }
    } catch (error) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    validateToken();
  }, []);

  const value = {
    user,
    setUser,
    loading,
    validateToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthProvider;