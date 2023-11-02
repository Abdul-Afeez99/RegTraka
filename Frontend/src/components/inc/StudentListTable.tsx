import { useStartAttendance, useStopAttendance } from "@/api/hooks";
import { CheckCircleIcon, XCircleIcon } from "@heroicons/react/24/solid";
import {
  Card,
  Table,
  TableHead,
  TableRow,
  TableHeaderCell,
  TableBody,
  TableCell,
  Text,
  Title,
  Badge,
  Button,
} from "@tremor/react";

export default function StudentListTable({
  data,
  course,
}: {
  data: {
    date: string;
    name: string;
    matric_no: string;
  }[];
  course: string;
}) {
  const { mutate: startAttendace, isLoading } = useStartAttendance();
  const { mutate: stopAttendance, isLoading: isStopAttendanceLoading } =
    useStopAttendance();
  return (
    <Card>
      <div className="flex justify-between items-center">
        <Title>List of {course} students</Title>
        <div className="flex gap-2">
          <Button
            onClick={() => startAttendace({ course })}
            loading={isLoading}
          >
            Start Attendance
          </Button>
          <Button
            onClick={() => stopAttendance({ course })}
            loading={isStopAttendanceLoading}
          >
            Stop Attendance
          </Button>
        </div>
      </div>
      <Table className="mt-5">
        <TableHead>
          <TableRow>
            <TableHeaderCell>S/N</TableHeaderCell>
            <TableHeaderCell>Name</TableHeaderCell>
            <TableHeaderCell>Matric No</TableHeaderCell>
            <TableHeaderCell>Attendance</TableHeaderCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data?.map((item, i) => {
            const present = true;
            return (
              <TableRow key={item.name}>
                <TableCell>{i + 1}</TableCell>
                <TableCell>{item.name}</TableCell>
                <TableCell>
                  <Text>{item.matric_no}</Text>
                </TableCell>
                <TableCell>
                  <Badge
                    color={present ? "emerald" : "red"}
                    icon={present ? CheckCircleIcon : XCircleIcon}
                  >
                    {item.date}
                  </Badge>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </Card>
  );
}
