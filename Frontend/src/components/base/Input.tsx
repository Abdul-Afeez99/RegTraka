import * as React from "react";

import {
  FieldErrors,
  FieldPath,
  FieldValues,
  UseFormRegister,
} from "react-hook-form";

function Label({ id, children }: { id: string; children: React.ReactNode }) {
  return (
    <label className="text-sm font-medium" htmlFor={id}>
      {children}
    </label>
  );
}
export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}
export interface ControlledInputProps<T extends FieldValues>
  extends InputProps {
  register: UseFormRegister<T>;
  name: FieldPath<T>;
  placeholder?: string;
  label?: string;
  errors?: FieldErrors<T>;
}

const ControlledInput = <T extends FieldValues>({
  register,
  name,
  placeholder,
  label,
  errors,
  ...props
}: ControlledInputProps<T>) => {
  const errorMessage = errors?.[name]?.message as string;
  return (
    <div className="flex flex-col w-full gap-2">
      <Label id={name}>{label}</Label>
      <div className="space-y-1">
        <input
          {...register(name)}
          className={
            "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50"
          }
          placeholder={placeholder}
          {...props}
        />
        {errorMessage && <p className="text-red-500 text-xs">{errorMessage}</p>}
      </div>
    </div>
  );
};

export default ControlledInput;
