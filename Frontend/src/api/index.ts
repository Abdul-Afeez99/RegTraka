import axios from "axios";
import { LoginResponse, SignupResponse } from "./types";
import useStore from "@/store";
const BASE_URL = "http://127.0.0.1:8000/";

const { getState } = useStore;
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

const tokenInterceptors = () => {
  const interceptor = api.interceptors.request.use(
    async (config) => {
      const access = getState().user?.access;
      config.headers["Authorization"] = `Bearer ${access}`;
      return config;
    },
    (error) => {
      Promise.reject(error);
    }
  );
  return () => api.interceptors.request.eject(interceptor);
};
// Response interceptor for API calls
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async function (error) {
    const {
      config: originalConfig,
      response: { status },
    } = error;
    originalConfig;
    const url = originalConfig.url;
    console.log(url);

    if (status === 401 && !originalConfig._retry) {
      originalConfig._retry = true;

      try {
        const tokens = await refreshAccessToken();
        const user = getState().user;
        if (user) {
          getState().setUser({ ...user, ...tokens });
        }
        axios.defaults.headers.common["Authorization"] =
          "Bearer " + tokens.access;
        return api(originalConfig);
      } catch (_error) {
        Promise.reject(_error);
      }
    }
    return Promise.reject(error);
  }
);

export async function refreshAccessToken() {
  const refresh = getState().user?.refresh;
  const response = await api.post<{
    access: string;
    refresh: string;
  }>("/api/token/refresh/", { refresh });
  return response.data;
}
export async function signup(data: {
  name: string;
  email: string;
  password: string;
}) {
  const response = await api.post<SignupResponse>(
    "administrator/sign_up",
    data
  );
  return response.data;
}

export async function login(data: { email: string; password: string }) {
  const response = await api.post<LoginResponse>("user/sign_in", data);
  return response.data;
}

export async function registerStudents(data: FormData) {
  const response = await api.post("/student/registration", data, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
}

export async function getAdminCourses() {
  const ejectInterceptor = tokenInterceptors();
  const response = await api.get<unknown[]>("administrator/courses");
  ejectInterceptor();
  return response.data;
}

export async function getAdminTotalStudents() {
  const ejectInterceptor = tokenInterceptors();

  const response = await api.get<{
    Total_Student: number;
  }>("administrator/total_students");
  ejectInterceptor();
  return response.data;
}

export async function getAdminInstructors() {
  const ejectInterceptor = tokenInterceptors();

  const response = await api.get<
    {
      name: string;
      gender: "MALE" | "FEMALE";
      email: string;
    }[]
  >("administrator/instructors");
  ejectInterceptor();
  return response.data;
}

export async function addInstructor(data: {
  name: string;
  email: string;
  gender: string;
  password: string;
}) {
  const ejectInterceptor = tokenInterceptors();
  const response = await api.post("/administrator/add_instructor", data);
  ejectInterceptor();
  return response.data;
}
export async function addClassroom(data: { name: string; year: number }) {
  const ejectInterceptor = tokenInterceptors();
  const response = await api.post("administrator/add-classroom", data);
  ejectInterceptor();
  return response.data;
}
export async function getAdminClassrooms() {
  const ejectInterceptor = tokenInterceptors();
  const response = await api.get<
    { id: number; name: "string"; year: number }[]
  >("administrator/list-classrooms");
  ejectInterceptor();
  return response.data;
}
export async function getSchools() {
  const response = await api.get<{ id: number; name: "string" }[]>(
    "get_available_schools"
  );
  return response.data;
}
