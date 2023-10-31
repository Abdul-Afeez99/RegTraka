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
  getClasses,
  getAvailableCourses,
  getInstructorCourses,
  getInstructorSchoolClasses,
  createInstructorCourse,
  getAttendance,
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
type GetClassesVariable = { schoolName: string };
export const useClasses = createQuery<
  Awaited<ReturnType<typeof getClasses>>,
  GetClassesVariable,
  Error
>({
  primaryKey: "classes",
  queryFn: ({ queryKey: [_, variables] }) => getClasses(variables.schoolName),
});
type GetAvailableCoursesVariable = {
  classroom: string;
  school: string;
};
export const useAvailableCourses = createQuery<
  Awaited<ReturnType<typeof getAvailableCourses>>,
  GetAvailableCoursesVariable,
  Error
>({
  primaryKey: "classes",
  queryFn: ({ queryKey: [_key, variables] }) => getAvailableCourses(variables),
});
// INSTRUCTOR ENDPOINTS

export const useInstructorCourses = createQuery({
  primaryKey: "instructor-courses",
  queryFn: getInstructorCourses,
});

type GetAttendanceVariable = {
  course: string;
};
export const useAttendance = createQuery<
  Awaited<ReturnType<typeof getAttendance>>,
  GetAttendanceVariable,
  Error
>({
  primaryKey: "instructor-attendance",
  queryFn: ({ queryKey: [_key, variables] }) => getAttendance(variables),
});
export const useInstructorSClasses = createQuery({
  primaryKey: "instructor-s-courses",
  queryFn: getInstructorSchoolClasses,
});
export const useCreateInstuctorCourse = createMutation({
  mutationFn: createInstructorCourse,
});
