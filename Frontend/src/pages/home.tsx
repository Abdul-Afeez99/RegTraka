import useStore from "@/store";
import React from "react";
import { Navigate } from "react-router-dom";

const Home = () => {
  const user = useStore((state) => state.user);

  if (user?.role === "instructor") {
    return <Navigate replace to="/instructor/dashboard" />;
  } else if (user?.role === "administrator") {
    return <Navigate replace to="/admin/dashboard" />;
  }
  return <Navigate replace to="/login" />;
};

export default Home;
