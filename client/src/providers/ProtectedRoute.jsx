import React, { useEffect, useState } from "react";
import apiClient from "../axiosConfig";

const ProtectedRoute = ({ children }) => {
  const [isValid, setIsValid] = useState(null);

  useEffect(() => {
    const validateToken = async () => {
      try {
        await apiClient.get("api/auth/validate");
        setIsValid(true);
      } catch (error) {
        setIsValid(false);
      }
    };

    validateToken();
  }, []);

  if (!isValid) {
    return <div>Carregando...</div>; // Exibe um estado de carregamento enquanto valida
  }

  return children; 
};

export default ProtectedRoute;