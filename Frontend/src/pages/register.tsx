import React from "react";
import { Flex, Text, Button, Title, Subtitle } from "@tremor/react";
import { toast } from "sonner";
import LoginImage from "@/assets/login.png";
import {
  useAvailableCourses,
  useClasses,
  useRegisterStudent,
  useSchools,
} from "@/api/hooks";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { MultiSelect, MultiSelectItem } from "@tremor/react";

const registerSchema = z.object({
  name: z.string().min(1, "Name is required"),
  matricNo: z.string().min(1, "MaticNo is required"),
  image: z.custom<FileList>((v) => v instanceof FileList, {
    message: "Image is required",
  }),
  gender: z.enum(["MALE", "FEMALE"]),
  school: z.string(),
  year: z.string(),
  course: z.array(z.string()),
});

type RegisterSchema = z.infer<typeof registerSchema>;

function Register() {
  const { data: schools } = useSchools({
    onSuccess: (data) => {
      setValue("school", data[0].name);
    },
  });

  const { mutateAsync, isLoading } = useRegisterStudent();
  const { register, handleSubmit, watch, reset, setValue } =
    useForm<RegisterSchema>({
      resolver: zodResolver(registerSchema),
      defaultValues: {
        school: "",
      },
    });
  // cohools && console.log(schools);
  const school = watch("school");
  const year = watch("year");

  const { data: classes } = useClasses({
    variables: { schoolName: school },
    enabled: school ? true : false,
    onSuccess: (data) => {
      setValue("year", data[0].name);
    },
  });
  const { data: courses } = useAvailableCourses({
    variables: { school, classroom: year },
    enabled: !!school && !!year,
    onSuccess: (data) => {
      setValue("course", [data[0]?.title]);
    },
  });
  const image = watch("image");
  const course = watch("course");
  const s = watch("school");
  console.log(s);
  let imagePreview: string | null = null;
  const firstImage = image?.[0];
  if (firstImage) {
    imagePreview = URL.createObjectURL(firstImage);
  }
  function onSubmit(data: RegisterSchema) {
    // build FormData for uploading image
    const schoolPk = schools?.find((s) => s.name === data.school)?.pk;
    const yearPk = classes?.find((s) => s.name === data.year)?.pk;
    const coursePk = data.course.map(
      (c) => courses?.find((s) => s.title === c)?.pk
    );
    const formData = new FormData();
    formData.append("gender", data.gender);
    formData.append("name", data.name);
    formData.append("matric_no", data.matricNo.toString());
    formData.append("image", data.image[0]);
    formData.append("school", schoolPk!);
    formData.append("year", yearPk!);
    formData.append("courses", coursePk!);
    //submit
    mutateAsync(formData)
      .then(() => {
        toast.success("Student Registered Successfully");
        reset({
          name: "",
          matricNo: "",
          gender: "MALE",
          school: "1",
          image: undefined,
        });
      })
      .catch((e) => toast.error(e.message));
  }
  return (
    <div className="grid grid-cols-2 min-h-screen container mx-auto px-6 items-center">
      <div className="grid grid-cols-2 min-h-screen fixed inset-0 -z-10">
        <div className="col-span-1 bg-white" />
        <div className="col-span-1 bg-[#e8f0ff]" />
      </div>
      <div className="max-w-sm justify-self-center py-8">
        <Title>Welcome to RegTraka</Title>
        <Subtitle>Please enter your details to register</Subtitle>
        <Flex
          alignItems="start"
          flexDirection="col"
          className="gap-2 mt-4 [&]>*:w-full "
        >
          <Flex alignItems="start" flexDirection="col">
            <Text>Name</Text>
            <input
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
            <Text>Matric No</Text>
            <input
              className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
              {...register("matricNo")}
            />
          </Flex>
          <Flex alignItems="start" flexDirection={"col"}>
            <Text>School</Text>
            <select
              {...register("school")}
              className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
            >
              {schools?.map(({ name }) => (
                <option value={name} key={name}>
                  {name}
                </option>
              ))}
            </select>
          </Flex>
          <Flex alignItems="start" flexDirection={"col"}>
            <Text>Year</Text>
            <select
              {...register("year")}
              className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
            >
              {classes?.map(({ name }) => (
                <option value={name} key={name}>
                  {name}
                </option>
              ))}
            </select>
          </Flex>

          <Flex alignItems="start" flexDirection={"col"}>
            <Text>Courses</Text>
            <MultiSelect
              value={course}
              onChange={(val) => setValue("course", val)}
            >
              {(courses ?? []).map((c) => (
                <MultiSelectItem value={c.title} key={c.title}>
                  {c.title}
                </MultiSelectItem>
              ))}
            </MultiSelect>
          </Flex>

          <Flex alignItems="start" flexDirection={"col"}>
            <Text>Image</Text>
            {firstImage && (
              <img src={imagePreview} className="" alt={"preview"} />
            )}
            <input
              type="file"
              id="file-ip-1"
              accept="image/*"
              className="rounded-lg border-gray-200 border py-1 pl-2 w-full"
              {...register("image")}
            ></input>
          </Flex>
          <Button
            loading={isLoading}
            className="mt-3"
            onClick={handleSubmit(onSubmit)}
          >
            Register
          </Button>
        </Flex>
      </div>
      <div className="justify-self-center max-h-screen sticky top-0">
        <img src={LoginImage} className="max-w-sm" height="500" width="500" />
      </div>
    </div>
  );
}

export default Register;
