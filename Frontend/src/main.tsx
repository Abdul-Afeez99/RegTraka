import React from "react";
import ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider,
  createRoutesFromElements,
  Route,
} from "react-router-dom";
import { Login, SignUp, Home } from "@/pages";
import "./index.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  InstructorAttendance,
  InstructorDashboard,
  InstructorRoot,
  InstructorStudents,
} from "@/pages/instructor";
import {
  AdminAttendance,
  AdminStudentsDetail,
  AdminDashboard,
  AdminInstructor,
  AdminRoot,
  AdminStudents,
} from "@/pages/admin";

import StudentList from "./pages/instructor/students/detail";
import Register from "./pages/register";
import { Toaster } from "sonner";

const queryClient = new QueryClient();

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" element={<Home />} />
      <Route path="login" element={<Login />} />
      <Route path="register-student" element={<Register />} />
      <Route path="signup" element={<SignUp />} />
      <Route path="instructor" element={<InstructorRoot />}>
        <Route path="dashboard" element={<InstructorDashboard />} />
        <Route path="students">
          <Route path="" element={<InstructorStudents />}></Route>
          <Route path=":courseId" element={<StudentList />}></Route>
        </Route>
        <Route path="attendance" element={<InstructorAttendance />} />
      </Route>
      <Route path="admin" element={<AdminRoot />}>
        <Route path="dashboard" element={<AdminDashboard />} />
        <Route path="students">
          <Route path="" element={<AdminStudents />}></Route>
          <Route path=":courseId" element={<AdminStudentsDetail />}></Route>
        </Route>
        <Route path="instructor" element={<AdminInstructor />} />
        <Route path="attendance" element={<InstructorAttendance />} />
      </Route>
    </>
  )
);
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <Toaster richColors />
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>
);
