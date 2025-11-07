import axios from "axios";
import { useMemo } from "react";

export function useApi() {
  return useMemo(
    () =>
      axios.create({
        baseURL: "/api/v1",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token") ?? ""}`
        }
      }),
    []
  );
}

