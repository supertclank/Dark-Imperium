import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { CharacterForm } from "../src/components/CharacterForm";
const { push, api } = vi.hoisted(() => ({ push: vi.fn(), api: vi.fn() }));
vi.mock("next/navigation", () => ({ useRouter: () => ({ push }) }));
vi.mock("../src/lib/api", () => ({ api }));
vi.mock("../src/components/Resource", () => ({
  useResource: (path: string) => ({
    data: [
      {
        id: path,
        name:
          path === "/species"
            ? "Human"
            : path === "/classes"
              ? "Guardsman"
              : "Lasgun",
        description: "Development content",
      },
    ],
    error: "",
  }),
  ResourceState: () => null,
}));
describe("character creation", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });
  it("submits selected content identifiers and opens the saved sheet", async () => {
    api.mockResolvedValue({ id: "saved-id" });
    render(<CharacterForm />);
    fireEvent.change(screen.getByLabelText("Character name"), {
      target: { value: "Cassian" },
    });
    for (const name of ["Human", "Guardsman", "Lasgun"])
      fireEvent.click(screen.getByRole("radio", { name: new RegExp(name) }));
    fireEvent.click(screen.getByRole("button", { name: /Save character/ }));
    await waitFor(() =>
      expect(push).toHaveBeenCalledWith("/characters/saved-id"),
    );
    expect(JSON.parse(api.mock.calls[0][1].body)).toEqual({
      name: "Cassian",
      speciesId: "/species",
      classId: "/classes",
      weaponId: "/weapons",
    });
  });
  it("retains the form and reports save failures", async () => {
    api.mockRejectedValue(new Error("The archive is unavailable."));
    render(<CharacterForm />);
    fireEvent.change(screen.getByLabelText("Character name"), {
      target: { value: "Cassian" },
    });
    for (const name of ["Human", "Guardsman", "Lasgun"])
      fireEvent.click(screen.getByRole("radio", { name: new RegExp(name) }));
    fireEvent.click(screen.getByRole("button", { name: /Save character/ }));
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "The archive is unavailable.",
    );
    expect(screen.getByLabelText("Character name")).toHaveValue("Cassian");
    expect(push).not.toHaveBeenCalled();
  });
});
