import axios, { type AxiosInstance, type InternalAxiosRequestConfig } from 'axios';

function getCSRFToken(): string | null {
  const name = 'csrftoken';
  let cookieValue: string | null = null;

  if (document.cookie) {
    const cookies: string[] = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie: string = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}

const api: AxiosInstance = axios.create({
  withCredentials: true,
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    if (!config.method) {
      return config;
    } else if (
      ['post', 'put', 'patch', 'delete'].includes(config.method.toLowerCase())
    ) {
      const csrfToken: string | null = getCSRFToken();
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
      }
    }
    return config;
  },

  (error: Error): Promise<never> => {
    return Promise.reject(error);
  },
);

export default api;
