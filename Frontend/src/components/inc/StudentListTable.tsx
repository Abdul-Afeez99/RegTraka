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
  console.log({ data });
  return (
    <Card>
      <Title>List of {course} students</Title>
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
