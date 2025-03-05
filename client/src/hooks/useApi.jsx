import { useState } from "react";

/**
 * Hook personalizado para comunicação com uma API RESTful.
 *
 * @param {string} baseUrl - A URL base da API.
 * @returns {Object} Um objeto contendo funções para CRUD e estados relacionados.
 */
const useApi = (baseUrl) => {
  const [data, setData] = useState(null); // Dados retornados pela API
  const [loading, setLoading] = useState(false); // Estado de carregamento
  const [error, setError] = useState(null); // Erro, se houver

  /**
   * Função para buscar dados da API.
   * @param {string} endpoint - O endpoint específico (ex.: '/sala').
   * @returns {Promise<void>}
   */
  const fetchData = async (endpoint) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${baseUrl}${endpoint}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      if (!response.ok) throw new Error("Erro ao buscar dados");
      const result = await response.json();
      setData(result);
      return result;
    } catch (err) {
      setError(err.erro);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Função para criar um novo recurso na API.
   * @param {string} endpoint - O endpoint específico (ex.: '/sala').
   * @param {Object} body - Os dados a serem enviados no corpo da requisição.
   * @returns {Promise<void>}
   */
  const createData = async (endpoint, body) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${baseUrl}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!response.ok) {
        const errorResponse = await response.json();
        throw new Error(errorResponse.erro || "Erro ao criar recurso");
      }
      const result = await response.json();
      setData((prevData) => [...(prevData || []), result]);
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Função para atualizar um recurso na API.
   * @param {string} endpoint - O endpoint específico (ex.: '/sala/1').
   * @param {Object} body - Os dados a serem enviados no corpo da requisição.
   * @returns {Promise<void>}
   */
  const updateData = async (endpoint, body) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${baseUrl}${endpoint}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!response.ok) throw new Error("Erro ao atualizar recurso");
      const result = await response.json();
      setData((prevData) =>
        prevData.map((item) => (item.id === result.id ? result : item))
      );
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Função para deletar um recurso na API.
   * @param {string} endpoint - O endpoint específico (ex.: '/sala/1').
   * @returns {Promise<void>}
   */
  const deleteData = async (endpoint) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${baseUrl}${endpoint}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Erro ao deletar recurso");
      setData((prevData) =>
        prevData.filter((item) => item.id !== endpoint.split("/").pop())
      );
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    data,
    loading,
    error,
    fetchData,
    createData,
    updateData,
    deleteData,
  };
};

export default useApi;
