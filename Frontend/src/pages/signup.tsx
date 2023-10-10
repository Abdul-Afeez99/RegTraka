import React from "react";
import { Flex, Text, Button } from "@tremor/react";
import SignUpImage from "@/assets/signup.png";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useSignup } from "@/api/hooks";
import { useNavigate } from "react-router-dom";
const signUpSchema = z.object({
  firstName: z.string().min(1, "First name is required").max(50),
  email: z.string().min(1, "Email is required").email(),
  password: z
    .string()
    .min(1, "Email is required")
    .min(12, "Password must be more than 11 characters")
    .max(50),
});

type SignUpSchema = z.infer<typeof signUpSchema>;

function SignUp() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignUpSchema>({
    resolver: zodResolver(signUpSchema),
  });
  console.log(errors);
  const { mutateAsync } = useSignup();
  const navigate = useNavigate();
  return (
    <div className="grid grid-cols-2 min-h-screen container mx-auto px-6 items-center">
      <div className="grid grid-cols-2 min-h-screen fixed inset-0 -z-10">
        <div className="col-span-1 bg-white" />
        <div className="col-span-1 bg-[#e8f0ff]" />
      </div>
      <div className="max-w-sm justify-self-center">
        <Heading size="6" className="">
          Welcome to RegTraka, Sign Up to Continue
        </Heading>
        <Text size="3" className="text-gray-500">
          kindly enter your details
        </Text>
        <Flex direction="column" gap={"2"} mt="5">
          <Flex direction={"column"}>
            <Text size={"1"} weight="medium">
              First Name
            </Text>
            <input
              type="text"
              className="rounded-lg border-gray-200 border py-1 pl-2"
              {...register("firstName")}
            />
          </Flex>
          <Flex direction={"column"}>
            <Text size={"1"} weight="medium">
              Email
            </Text>
            <input
              type="email"
              className="rounded-lg border-gray-200 border py-1 pl-2"
              {...register("email")}
            />
          </Flex>
          <Flex direction={"column"}>
            <Text size={"1"} weight="medium">
              Password
            </Text>
            <input
              type="password"
              className="rounded-lg border-gray-200 border py-1 pl-2"
              {...register("password")}
            />
          </Flex>
          <Button
            mt="3"
            onClick={handleSubmit((data) => {
              mutateAsync({
                name: data.firstName,
                email: data.email,
                password: data.password,
              }).then(() => navigate("/login"));
            })}
          >
            Sign Up
          </Button>
        </Flex>
      </div>
      <div className="justify-self-center">
        <img src={SignUpImage} className="max-w-sm" height="500" width="500" />
      </div>
    </div>
  );
}

export default SignUp;
