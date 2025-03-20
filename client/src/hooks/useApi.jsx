import { useState } from "react"; 
import apiClient from "../axiosConfig";

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
      const response = await apiClient.get(`${baseUrl}${endpoint}`, {
        headers: { "Content-Type": "application/json" },
      });
      setData(response.data)
      return response.data
    } catch (err) {
      setError(err.response?.data?.erro || err.message);
      throw new Error(err.response?.data?.erro);
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
      const response = await apiClient.post(`${baseUrl}${endpoint}`, body, {
        headers: { "Content-Type": "application/json" }
      });
      setData((prevData) => [...(prevData || []), response.data]);
    } catch (err) {
      setError(err.response?.data?.erro || err.message);
      throw new Error(err.response?.data?.erro);
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
      await apiClient.put(`${baseUrl}${endpoint}`, body, {
        headers: { "Content-Type": "application/json" }
      });
    } catch (err) {
      setError(err.response?.data?.erro || err.message);
      throw new Error(err.response?.data?.erro);
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
      await apiClient.delete(`${baseUrl}${endpoint}`);
    } catch (err) {
      setError(err.response?.data?.erro || err.message);
      throw new Error(err.response?.data?.erro);
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
