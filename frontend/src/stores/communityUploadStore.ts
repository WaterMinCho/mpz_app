import { create } from "zustand";
import { persist, type PersistStorage } from "zustand/middleware";
import type { PetCardAnimal } from "@/types/animal";
import { safeSetItem, safeGetItem, safeRemoveItem } from "@/lib/storage-utils";

// PetCardAnimal을 확장한 타입 (adoptionId 포함)
type ExtendedPetCardAnimal = PetCardAnimal & { adoptionId?: string };

type PublicType = "center" | "public";

interface CommunityUploadState {
  title: string;
  content: string;
  selectedPet: ExtendedPetCardAnimal | null;
  tags: string[];
  publicType: PublicType;

  setTitle: (title: string) => void;
  setContent: (content: string) => void;
  setSelectedPet: (pet: ExtendedPetCardAnimal | null) => void;
  setTags: (tags: string[]) => void;
  setPublicType: (type: PublicType) => void;
  updateForm: (data: {
    title?: string;
    content?: string;
    selectedPet?: ExtendedPetCardAnimal | null;
    tags?: string[];
    publicType?: PublicType;
  }) => void;
  reset: () => void;
}

const initialState = {
  title: "",
  content: "",
  selectedPet: null,
  tags: [],
  publicType: "center" as PublicType,
};

// 앱 환경에서도 작동하는 커스텀 storage
const customStorage = {
  getItem: (name: string): string | null => {
    return safeGetItem(name);
  },
  setItem: (name: string, value: string): void => {
    safeSetItem(name, value);
  },
  removeItem: (name: string): void => {
    safeRemoveItem(name);
  },
} as unknown as PersistStorage<CommunityUploadState>;

export const useCommunityUploadStore = create<CommunityUploadState>()(
  persist(
    (set) => ({
      ...initialState,
      setTitle: (title) => set({ title }),
      setContent: (content) => set({ content }),
      setSelectedPet: (selectedPet) => set({ selectedPet }),
      setTags: (tags) => set({ tags }),
      setPublicType: (publicType) => set({ publicType }),
      updateForm: (data) => set((state) => ({ ...state, ...data })),
      reset: () => set(initialState),
    }),
    {
      name: "community-upload-draft",
      version: 1,
      storage: customStorage,
    }
  )
);
