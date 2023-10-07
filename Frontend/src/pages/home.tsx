import useStore from "@/store";
import React from "react";
import { Navigate } from "react-router-dom";

const Home = () => {
  const user = useStore((state) => state.user);
  if (user) {
    return <Navigate replace to="/dashboard" />;
  }
  return <Navigate replace to="/login" />;
};

export default Home;
