import useStore from "@/store";
import React from "react";
import { Navigate, Link, useParams } from "react-router-dom";
import { Button } from "@tremor/react";
import StudentListTable from "@/components/inc/StudentListTable";
import StudentYearTable from "@/components/inc/StudentYearTable";

function StudentList() {
  const params = useParams();
  console.log(params);
  return (
    <section className="px-5 my-8 flex flex-col gap-8">
      <StudentYearTable classroom={params?.courseId ?? ""} />
    </section>
  );
}

export default StudentList;
