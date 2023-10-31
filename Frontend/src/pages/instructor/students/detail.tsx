import useStore from "@/store";
import React from "react";
import { Navigate, Link, useParams } from "react-router-dom";
import { Button } from "@tremor/react";
import StudentListTable from "@/components/inc/StudentListTable";
import { useAttendance } from "@/api/hooks";

function StudentList() {
  const params = useParams();
  const course = params?.courseId ?? "";
  const { data: attendance } = useAttendance({
    variables: {
      course,
    },
  });
  return (
    <section className="px-5 my-8 flex flex-col gap-8">
      <StudentListTable data={attendance} {...{ course }} />
    </section>
  );
}

export default StudentList;
