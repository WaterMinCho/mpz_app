/**
 * 종(breed) + 이름(name) 표시 로직
 *
 * 1. 종 있고 이름 있을 때: "믹스견(깜돌이)"
 * 2. 종 있고 이름 없을 때: "믹스견"
 * 3. 종 없고 이름 있을 때: "깜돌이"
 * 4. 종 없고 이름 없을 때: "종 미등록"
 */
export function getDisplayBreedName(
  breed: string | null | undefined,
  name: string | null | undefined
): string {
  const hasBreed = !!breed?.trim();
  const hasName = !!name && !name.startsWith("공공데이터_");

  if (hasBreed && hasName) return `${breed}(${name})`;
  if (hasBreed) return breed!;
  if (hasName) return name;
  return "종 미등록";
}
