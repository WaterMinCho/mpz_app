import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from "axios";

// 환경 변수에서 API 베이스 URL 가져오기
// NEXT_PUBLIC_ 접두사가 있어야 클라이언트 측에서 접근 가능
const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000/v1/";

const instance: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
});

instance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

export default instance;
