import axios from "axios";
import { LoginResponse, SignupResponse } from "./types";
const BASE_URL = "http://127.0.0.1:8000/";

const api = axios.create({
	baseURL: BASE_URL,
	headers: {
		"Content-Type": "application/json",
	},
});

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
