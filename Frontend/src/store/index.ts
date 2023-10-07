import { persist, subscribeWithSelector, devtools } from "zustand/middleware";
import { create, StateCreator as ZStateCreator } from "zustand";
import createUserSlice, { type UserSlice } from "./slices/user";

export type Slices = UserSlice;
export type StateCreator<T> = ZStateCreator<Slices, [], [], T>;
const useStore = create<Slices>()(
  subscribeWithSelector(
    persist(
      devtools((...a) => ({
        ...createUserSlice(...a),
      })),
      {
        name: "store",
        partialize: (state) =>
          Object.fromEntries(
            Object.entries(state).filter(
              ([key]) =>
                !["searchOpen", "time", "sideBarOpen", "activeToasts"].includes(
                  key
                )
            )
          ),
      }
    )
  )
);
export default useStore;
