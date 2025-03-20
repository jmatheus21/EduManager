import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:5173",
  withCredentials: true, // Permite enviar cookies com as requisições
  headers: {
    "Content-Type": "application/json",
  }
});

// Interceptador de Resposta
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // Redireciona para a página de login se o token for inválido ou expirado
      window.location.href = "/login"; // Redireciona para a página de login
    }
    return Promise.reject(error);
  }
);

export default apiClient;