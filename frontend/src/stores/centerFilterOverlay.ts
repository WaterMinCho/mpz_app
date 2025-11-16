import { create } from "zustand";

interface CenterFilterOverlayState {
  isOpen: boolean;
  open: () => void;
  close: () => void;
}

export const useCenterFilterOverlayStore = create<CenterFilterOverlayState>(
  (set) => ({
    isOpen: false,
    open: () => set({ isOpen: true }),
    close: () => set({ isOpen: false }),
  })
);
