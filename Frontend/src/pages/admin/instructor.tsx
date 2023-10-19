import { useAddInstructors, useAdminInstructors } from "@/api/hooks";
import { PlusIcon } from "@heroicons/react/24/solid";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Button,
  Card,
  Flex,
  Subtitle,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeaderCell,
  TableRow,
  Text,
  Title,
} from "@tremor/react";
import React from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { toast } from "sonner";
import { useQueryClient } from "@tanstack/react-query";
import Modal from "@/components/base/Modal";

function Instructor() {
  const { data, isLoading } = useAdminInstructors();
  const [open, setOpen] = React.useState(false);

  return (
    <div className="p-4">
      <Modal open={open} onOpenChange={setOpen}>
        <AddInstructorForm />
      </Modal>
      <Card>
        <div className="flex items-center justify-between">
          <Title>List of Intructors</Title>
          <Button icon={PlusIcon} onClick={() => setOpen(true)}>
            Add instructiors
          </Button>
        </div>
        {isLoading ? (
          <Subtitle>Loading...</Subtitle>
        ) : (
          <Table className="mt-5">
            <TableHead>
              <TableRow>
                <TableHeaderCell>S/N</TableHeaderCell>
                <TableHeaderCell>Name</TableHeaderCell>
                <TableHeaderCell>Sex</TableHeaderCell>
                <TableHeaderCell>Email</TableHeaderCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data?.map((item, i) => {
                return (
                  <TableRow key={item.name}>
                    <TableCell>{i + 1}</TableCell>
                    <TableCell>{item.name}</TableCell>
                    <TableCell>
                      <Text>{item.gender.toLocaleLowerCase()}</Text>
                    </TableCell>
                    <TableCell>
                      <Text>{item.email.toLocaleLowerCase()}</Text>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        )}
      </Card>
    </div>
  );
}

const instructorSchema = z.object({
  name: z.string().min(1, "First name is required").max(50),
  email: z.string().min(1, "Email is required").email(),
  gender: z.enum(["MALE", "FEMALE"]),

  password: z
    .string()
    .min(1, "Email is required")
    .min(12, "Password must be more than 11 characters")
    .max(50),
});

type InstructorSchema = z.infer<typeof instructorSchema>;

function AddInstructorForm() {
  const { register, handleSubmit, reset } = useForm<InstructorSchema>({
    resolver: zodResolver(instructorSchema),
  });
  const { mutateAsync, isLoading } = useAddInstructors();
  const queryClient = useQueryClient();
  return (
    <div className="flex flex-col gap-4">
      <Title>Add Instructor Details</Title>
      <Flex
        alignItems="start"
        flexDirection="col"
        className="gap-2 mt-4 [&]>*:w-full "
      >
        <Flex alignItems="start" flexDirection="col">
          <Text>Name</Text>
          <input
            type="text"
            className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
            {...register("name")}
          />
        </Flex>
        <Flex alignItems="start" flexDirection={"col"}>
          <Text>Gender</Text>
          <select
            {...register("gender")}
            className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
          >
            <option value="MALE">Male</option>
            <option value="FEMALE">Female</option>
          </select>
        </Flex>
        <Flex alignItems="start" flexDirection="col">
          <Text>Email</Text>
          <input
            type="email"
            className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
            {...register("email")}
          />
        </Flex>
        <Flex alignItems="start" flexDirection="col">
          <Text>Password</Text>
          <input
            type="password"
            className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
            {...register("password")}
          />
        </Flex>
        <Button
          className="mt-3"
          loading={isLoading}
          onClick={handleSubmit((data) => {
            mutateAsync(data).then(() => {
              toast.success("Instructor created successfully");
              queryClient.invalidateQueries(useAdminInstructors.getKey());
              reset({
                name: "",
                gender: "MALE",
                email: "",
                password: "",
              });
            });
          })}
        >
          Add Instructor
        </Button>
      </Flex>
    </div>
  );
}

export default Instructor;
