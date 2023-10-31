import {
  useCreateInstuctorCourse,
  useInstructorCourses,
  useInstructorSClasses,
} from "@/api/hooks";
import ControlledInput from "@/components/base/Input";
import Modal from "@/components/base/Modal";
import { PlusIcon } from "@heroicons/react/24/solid";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQueryClient } from "@tanstack/react-query";
import { Button, Flex, Text, Title } from "@tremor/react";
import React from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import { toast } from "sonner";
import { z } from "zod";

function Students() {
  const { data: instructorCourses } = useInstructorCourses();
  const [open, setOpen] = React.useState(false);
  return (
    <section className="px-5 my-8">
      <Modal open={open} onOpenChange={setOpen}>
        <AddInstructorForm />
      </Modal>
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold">View Students</h1>
        <Button icon={PlusIcon} onClick={() => setOpen(true)}>
          Add Courses
        </Button>
      </div>
      <p>Select course and see students studying course </p>
      <div className="flex flex-col gap-4">
        {instructorCourses?.courses?.map((course) => (
          <Courses key={course.title} course={course.title} />
        ))}
      </div>
    </section>
  );
}
function Courses({ course }: { course: string }) {
  return (
    <section className="px-4 py-6 rounded-md bg-primary/30 flex justify-between items-center">
      <h2>
        <span className="font-bold text-lg ">{course} </span>
      </h2>
      <Button>
        <Link to={`/instructor/students/${course}`}>View Details</Link>
      </Button>
    </section>
  );
}
const instructorSchema = z.object({
  title: z.string().min(1, "Title is required").max(50),
  year: z.string().min(1, "Year is required"),
  credit: z.string().min(1, "Credit is required"),
});

type InstructorSchema = z.infer<typeof instructorSchema>;

function AddInstructorForm() {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<InstructorSchema>({
    resolver: zodResolver(instructorSchema),
  });
  const { data: years } = useInstructorSClasses();
  const { mutateAsync, isLoading } = useCreateInstuctorCourse();
  const queryClient = useQueryClient();

  return (
    <div className="flex flex-col gap-4">
      <Title>Add Instructor Details</Title>
      <Flex
        alignItems="start"
        flexDirection="col"
        className="gap-2 mt-4 [&]>*:w-full "
      >
        <ControlledInput
          name="title"
          label="Title"
          register={register}
          placeholder="Enter Title"
          errors={errors}
        />
        {/* <Flex alignItems="start" flexDirection="col">
            <Text>Title</Text>
            <input
              type="text"
              className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
              {...register("title")}
            />
          </Flex> */}
        <Flex alignItems="start" flexDirection={"col"}>
          <Text>Year</Text>
          <select
            {...register("year")}
            className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
          >
            {years?.map((year) => (
              <option key={year.id} value={year.year}>
                {year.name}
              </option>
            ))}
          </select>
        </Flex>
        <ControlledInput
          name="credit"
          label="Credit"
          register={register}
          placeholder="Enter Credit"
          errors={errors}
        />

        <Button
          className="mt-3"
          loading={isLoading}
          onClick={handleSubmit((data) => {
            mutateAsync({
              ...data,
              year: parseInt(data.year),
              credit: parseInt(data.credit),
            }).then(() => {
              toast.success("Course  created successfully");
              queryClient.invalidateQueries(useInstructorCourses.getKey());
              reset({
                title: "",
                year: "",
                credit: "",
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

export default Students;
