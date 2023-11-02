import { useAttendance } from "@/api/hooks";
import StudentListTable from "@/components/inc/StudentListTable";
import { useParams } from "react-router-dom";

function StudentList() {
  const params = useParams();
  const course = params?.courseId ?? "";
  const { data: attendance, refetch } = useAttendance({
    variables: {
      course,
    },
  });
  return (
    <section className="px-5 my-8 flex flex-col gap-8">
      <StudentListTable
        data={attendance ?? []}
        {...{ course }}
        refetch={refetch}
      />
    </section>
  );
}

export default StudentList;
