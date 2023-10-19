import { createMutation, createQuery } from "react-query-kit";
import {
  login,
  signup,
  registerStudents,
  getAdminCourses,
  getAdminTotalStudents,
  getAdminInstructors,
  addInstructor,
  getAdminClassrooms,
  addClassroom,
  getSchools,
} from "..";

export const useSignup = createMutation({
  mutationFn: signup,
});
export const useLogin = createMutation({
  mutationFn: login,
});
export const useRegisterStudent = createMutation({
  mutationFn: registerStudents,
});
export const useAdminCourses = createQuery({
  primaryKey: "adminCourses",
  queryFn: getAdminCourses,
});
export const useAdminTotalStudents = createQuery({
  primaryKey: "adminTotalStudents",
  queryFn: getAdminTotalStudents,
});
export const useAdminInstructors = createQuery({
  primaryKey: "adminInstructors",
  queryFn: getAdminInstructors,
});

export const useAddInstructors = createMutation({
  mutationFn: addInstructor,
});
export const useAddClassroom = createMutation({
  mutationFn: addClassroom,
});
export const useAdminClassrooms = createQuery({
  primaryKey: "adminClassrooms",
  queryFn: getAdminClassrooms,
});
export const useSchools = createQuery({
  primaryKey: "schools",
  queryFn: getSchools,
});
