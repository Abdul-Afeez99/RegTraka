import useStore from "@/store";
import React from "react";
import { Navigate, Link } from "react-router-dom";
import { sampleCourses } from "@/data";
import { Button, Title, Text, Flex } from "@tremor/react";
import { useAddClassroom, useAdminClassrooms } from "@/api/hooks";
import { PlusIcon } from "@heroicons/react/24/solid";
import Modal from "@/components/base/Modal";
import { toast } from "sonner";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQueryClient } from "@tanstack/react-query";

function Students() {
  const { data: courses, isLoading } = useAdminClassrooms();
  const [open, setOpen] = React.useState(false);

  console.log(courses);
  return (
    <section className="px-5 my-8">
      <Modal open={open} onOpenChange={setOpen}>
        <AddInstructorForm />
      </Modal>
      <div className="flex items-center justify-between">
        <Title>List of Levels</Title>
        <Button icon={PlusIcon} onClick={() => setOpen(true)}>
          Add Levels
        </Button>
      </div>
      <p>Select level and see students studying in the level </p>
      <div className="flex flex-col gap-4">
        {isLoading ? (
          <p className="fong-bold text-lg">Loading...</p>
        ) : (
          <>
            {courses?.map((course) => (
              <Courses key={course.name} year={course.year} />
            ))}
          </>
        )}
      </div>
    </section>
  );
}
function Courses({ year }: { year: number }) {
  return (
    <section className="px-4 py-6 rounded-md bg-primary/30 flex justify-between items-center">
      <h2>
        <span className="font-bold text-lg ">{year} </span>
        <span className="font-medium text-md">level</span>
      </h2>
      <Button>
        <Link to={`/admin/students/${year}`}>View Details</Link>
      </Button>
    </section>
  );
}

const levelSchema = z.object({
  name: z.string().min(1, "First name is required").max(50),
  year: z.string(),
});

type LevelSchema = z.infer<typeof levelSchema>;

function AddInstructorForm() {
  const { register, handleSubmit, reset } = useForm<LevelSchema>({
    resolver: zodResolver(levelSchema),
  });
  const { mutateAsync, isLoading } = useAddClassroom();
  const queryClient = useQueryClient();
  return (
    <div className="flex flex-col gap-4">
      <Title>Add Classroom Details</Title>
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
        <Flex alignItems="start" flexDirection="col">
          <Text>Year</Text>
          <input
            type="number"
            className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
            {...register("year")}
          />
        </Flex>

        <Button
          className="mt-3"
          loading={isLoading}
          onClick={handleSubmit((data) => {
            mutateAsync({ ...data, year: parseInt(data.year) }).then(() => {
              toast.success("Instructor created successfully");
              queryClient.invalidateQueries(useAddClassroom.getKey());
              reset({
                name: "",
                year: undefined,
              });
            });
          })}
        >
          Add Classroom
        </Button>
      </Flex>
    </div>
  );
}
export default Students;
