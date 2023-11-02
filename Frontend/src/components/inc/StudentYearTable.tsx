import { useGetStudentList } from "@/api/hooks";
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
} from "@tremor/react";

export default function StudentYearTable({ classroom }: { classroom: string }) {
  const { data: students } = useGetStudentList({
    variables: {
      classroom,
    },
  });
  return (
    <Card>
      <div className="flex justify-between items-center">
        <Title>List of {classroom} students</Title>
      </div>
      <Table className="mt-5">
        <TableHead>
          <TableRow>
            <TableHeaderCell>S/N</TableHeaderCell>
            <TableHeaderCell>Name</TableHeaderCell>
            <TableHeaderCell>Gender</TableHeaderCell>
            <TableHeaderCell>Matric No</TableHeaderCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {students?.map((item, i) => {
            return (
              <TableRow key={item.name}>
                <TableCell>{i + 1}</TableCell>
                <TableCell>{item.name}</TableCell>
                <TableCell>
                  <Text>{item.gender}</Text>
                </TableCell>
                <TableCell>
                  <Text>{item.matric_no}</Text>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </Card>
  );
}
