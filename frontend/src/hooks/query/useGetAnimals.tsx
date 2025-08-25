import { useInfiniteQuery, useQuery } from "@tanstack/react-query";
import instance from "@/lib/axios-instance";
import {
  Animal,
  GetAnimalsParams,
  RawAnimalResponse,
  ActualGetAnimalsResponse,
} from "@/types/animal";

const getAnimals = async (
  params?: GetAnimalsParams
): Promise<ActualGetAnimalsResponse> => {
  const searchParams = new URLSearchParams();

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, value.toString());
      }
    });
  }

  const endpoint = `/animals/?${searchParams.toString()}`;
  const response = await instance.get<ActualGetAnimalsResponse>(endpoint);

  // API 응답의 snake_case를 camelCase로 변환
  const transformedResponse: ActualGetAnimalsResponse = {
    ...response.data,
    data: response.data.data.map((animal) => ({
      id: animal.id,
      name: animal.name,
      is_female: animal.is_female,
      age: animal.age,
      weight: animal.weight,
      color: animal.color,
      breed: animal.breed,
      description: animal.description,
      status: animal.status,
      waiting_days: animal.waiting_days,
      activity_level: animal.activity_level,
      sensitivity: animal.sensitivity,
      sociability: animal.sociability,
      separation_anxiety: animal.separation_anxiety,
      special_notes: animal.special_notes,
      health_notes: animal.health_notes,
      basic_training: animal.basic_training,
      trainer_comment: animal.trainer_comment,
      announce_number: animal.announce_number,
      announcement_date: animal.announcement_date,
      admission_date: animal.admission_date,
      found_location: animal.found_location,
      personality: animal.personality,
      center_id: animal.center_id,
      animal_images: animal.animal_images || [],
      created_at: animal.created_at,
      updated_at: animal.updated_at,
    })),
  };

  return transformedResponse;
};

export const useGetAnimals = (params?: GetAnimalsParams) => {
  return useInfiniteQuery({
    queryKey: ["animals", params],
    queryFn: ({ pageParam = 1 }) => getAnimals({ ...params, page: pageParam }),
    getNextPageParam: (lastPage) => {
      if (lastPage.nextPage !== null) {
        return lastPage.nextPage;
      }
      return undefined;
    },
    initialPageParam: 1,
    staleTime: 3 * 60 * 1000, // 3분
    gcTime: 10 * 60 * 1000, // 10분
    retry: 1,
    refetchOnWindowFocus: false,
  });
};

/** @TODO pet image GET query 추가 */

export const useGetBreeds = () => {
  return useQuery({
    queryKey: ["breeds"],
    queryFn: async () => {
      return instance.get("/breeds/");
    },
    staleTime: 5 * 60 * 1000, // 5분
    gcTime: 10 * 60 * 1000, // 10분
  });
};

/** @TODO pet image GET query 추가 */

export const useGetAnimalById = (animalId: string) => {
  return useQuery({
    queryKey: ["animals", animalId],
    queryFn: async (): Promise<Animal> => {
      const response = await instance.get<RawAnimalResponse>(
        `/animals/${animalId}/`
      );

      // API 응답의 snake_case를 camelCase로 변환
      const rawAnimal = response.data;
      return {
        id: rawAnimal.id,
        name: rawAnimal.name,
        isFemale: rawAnimal.is_female,
        age: rawAnimal.age,
        weight: rawAnimal.weight,
        color: rawAnimal.color,
        breed: rawAnimal.breed,
        description: rawAnimal.description,
        status: rawAnimal.status,
        waitingDays: rawAnimal.waiting_days,
        activityLevel: rawAnimal.activity_level,
        sensitivity: rawAnimal.sensitivity,
        sociability: rawAnimal.sociability,
        separationAnxiety: rawAnimal.separation_anxiety,
        specialNotes: rawAnimal.special_notes,
        healthNotes: rawAnimal.health_notes,
        basicTraining: rawAnimal.basic_training,
        trainerComment: rawAnimal.trainer_comment,
        announceNumber: rawAnimal.announce_number,
        announcementDate: rawAnimal.announcement_date,
        admissionDate: rawAnimal.admission_date,
        foundLocation: rawAnimal.found_location,
        personality: rawAnimal.personality,
        centerId: rawAnimal.center_id,
        animalImages: rawAnimal.animal_images || [],
        createdAt: rawAnimal.created_at,
        updatedAt: rawAnimal.updated_at,
      };
    },
    enabled: !!animalId,
    staleTime: 3 * 60 * 1000, // 3분
    gcTime: 10 * 60 * 1000, // 10분
  });
};

// 거리 기반 관련 동물 조회 훅
export const useGetRelatedAnimalsByDistance = (animalId?: string) => {
  return useQuery({
    queryKey: ["relatedAnimals", animalId],
    queryFn: async () => {
      if (!animalId) {
        throw new Error("동물 ID가 필요합니다");
      }

      return instance.get(`/animals/${animalId}/related_by_distance/?limit=6`);
    },
    staleTime: 5 * 60 * 1000, // 5분
    gcTime: 10 * 60 * 1000, // 10분
    retry: 1,
    refetchOnWindowFocus: false,
    enabled: !!animalId, // animalId가 있을 때만 실행
  });
};
