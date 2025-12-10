import axios from "axios";
import { useMemo } from "react";

export function useApi() {
  return useMemo(
    () =>
      axios.create({
        baseURL: "http://localhost:8000/api/v1",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token") ?? ""}`,
          // Content-Type yahan mat do – axios khud set karega
        },
        withCredentials: true,
      }),
    []
  );
}
