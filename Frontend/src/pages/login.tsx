import React from "react";
import { Flex, Text, Button, Title, Subtitle } from "@tremor/react";

import LoginImage from "@/assets/login.png";
import { useLogin } from "@/api/hooks";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import useStore from "@/store";
import { isAxiosError } from "axios";
import { toast } from "sonner";
import ControlledInput from "@/components/base/Input";
const loginSchema = z.object({
  email: z.string().min(1, "Email is required").email(),
  password: z.string().min(1, "Email is required"),
});

type LoginSchema = z.infer<typeof loginSchema>;

function Login() {
  const setUser = useStore((state) => state.setUser);
  const navigate = useNavigate();
  const { mutateAsync, isLoading } = useLogin({
    onError: (error) => {
      if (isAxiosError(error)) {
        toast.error(error.message);
      }
    },
    onSuccess: (data) => {
      setUser(data);
      if (data.role === "administrator") {
        navigate("/admin/dashboard");
      } else {
        navigate("/instructor/dashboard");
      }
    },
  });
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginSchema>({
    resolver: zodResolver(loginSchema),
  });
  return (
    <div className="grid grid-cols-2 min-h-screen container mx-auto px-6 items-center">
      <div className="grid grid-cols-2 min-h-screen fixed inset-0 -z-10">
        <div className="col-span-1 bg-white" />
        <div className="col-span-1 bg-[#e8f0ff]" />
      </div>
      <div className="max-w-sm justify-self-center">
        <Title>Welcome to RegTraka, Sign In to Continue</Title>
        <Subtitle>Please enter your details</Subtitle>
        <Flex
          alignItems="start"
          flexDirection="col"
          className="gap-2 mt-4 [&]>*:w-full "
        >
          <ControlledInput
            name="email"
            label="Email"
            register={register}
            placeholder="Enter Email"
            errors={errors}
          />
          <ControlledInput
            name="password"
            label="Password"
            register={register}
            placeholder="Enter Password"
            errors={errors}
          />

          <Button
            loading={isLoading}
            className="mt-3"
            onClick={handleSubmit((d) =>
              mutateAsync(d).then((d) => console.log(d))
            )}
          >
            Sign In
          </Button>
        </Flex>
      </div>
      <div className="justify-self-center">
        <img src={LoginImage} className="max-w-sm" height="500" width="500" />
      </div>
    </div>
  );
}

export default Login;
