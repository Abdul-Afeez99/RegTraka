import { createMutation } from "react-query-kit";
import { login, signup, registerStudents } from "..";

export const useSignup = createMutation({
	mutationFn: signup,
});
export const useLogin = createMutation({
	mutationFn: login,
});
export const useRegisterStudent = createMutation({
	mutationFn: registerStudents,
});
