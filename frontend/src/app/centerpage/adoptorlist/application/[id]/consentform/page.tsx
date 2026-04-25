"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft } from "@phosphor-icons/react";

import { Container } from "@/components/common/Container";
import { TopBar } from "@/components/common/TopBar";
import { IconButton } from "@/components/ui/IconButton";
import { FormListItem } from "@/components/ui/FormListItem";
import { useGetCenterAdoption, useGetConsents } from "@/hooks";

interface ConsentFormPageProps {
  params: Promise<{ id: string }>;
}

function getErrorMessage(error: unknown) {
  if (!error) return "정보를 불러오는 중 오류가 발생했어요.";
  // error.message를 사용자에게 직접 노출하지 않고, 친화적 문구로 통일
  console.error("동의서 로딩 에러:", error);
  return "정보를 불러오는 중 오류가 발생했어요. 다시 시도해주세요.";
}

export default function ConsentFormPage({ params }: ConsentFormPageProps) {
  const router = useRouter();
  const { id } = React.use(params);

  const {
    data: adoptionDetail,
    isLoading: isAdoptionLoading,
    error: adoptionError,
  } = useGetCenterAdoption(id);

  const {
    data: consents,
    isLoading: isConsentsLoading,
    error: consentsError,
  } = useGetConsents();

  const activeConsents = React.useMemo(
    () => consents?.filter((consent) => consent.is_active) ?? [],
    [consents]
  );
  const fallbackConsent = React.useMemo(
    () => activeConsents[0] ?? consents?.[0] ?? null,
    [activeConsents, consents]
  );

  const isLoading = isAdoptionLoading || isConsentsLoading;
  const hasError = adoptionError || consentsError;
  const errorMessage = getErrorMessage(adoptionError ?? consentsError);

  const handleBack = () => {
    router.back();
  };

  if (isLoading) {
    return (
      <Container className="min-h-screen pb-28">
        <TopBar
          variant="variant4"
          left={
            <div className="flex items-center gap-2">
              <IconButton
                icon={({ size }) => <ArrowLeft size={size} weight="bold" />}
                size="iconM"
                onClick={handleBack}
              />
              <h4>동의서 보기</h4>
            </div>
          }
        />
        <div className="mx-4 mt-4.5 flex flex-col gap-6">
          <div className="py-10 text-center text-gr">불러오는 중입니다...</div>
        </div>
      </Container>
    );
  }

  if (hasError) {
    return (
      <Container className="min-h-screen pb-28">
        <TopBar
          variant="variant4"
          left={
            <div className="flex items-center gap-2">
              <IconButton
                icon={({ size }) => <ArrowLeft size={size} weight="bold" />}
                size="iconM"
                onClick={handleBack}
              />
              <h4>동의서 보기</h4>
            </div>
          }
        />
        <div className="mx-4 mt-4.5 flex flex-col gap-6">
          <div className="py-10 text-center text-red-500">{errorMessage}</div>
        </div>
      </Container>
    );
  }

  return (
    <div className="min-h-screen bg-bg">
      <Container className="min-h-screen pb-28">
        <TopBar
          variant="variant4"
          left={
            <div className="flex items-center gap-2">
              <IconButton
                icon={({ size }) => <ArrowLeft size={size} weight="bold" />}
                size="iconM"
                onClick={handleBack}
              />
              <h4>동의서 보기</h4>
            </div>
          }
        />
        <div className="mx-4 mt-4.5 flex flex-col gap-8">
          <div className="flex flex-col gap-4">
            <div className="flex flex-col gap-1">
              <h2 className="text-bk">
                {fallbackConsent?.title ?? "센터 동의서 목록"}
              </h2>
              <p className="body2 text-gr">
                {fallbackConsent?.description ??
                  "센터에서 현재 사용 중인 동의서 내용을 확인해주세요."}
              </p>
            </div>
            {fallbackConsent ? (
              <div className="flex flex-col gap-6">
                {(activeConsents.length > 0
                  ? activeConsents
                  : consents ?? []
                ).map((consent) => (
                  <div
                    key={consent.id}
                    className="body text-dg whitespace-pre-wrap leading-relaxed"
                  >
                    {consent.content}
                  </div>
                ))}
              </div>
            ) : (
              <div className="rounded-2xl border border-lg bg-white px-4 py-6 text-center text-gr">
                등록된 동의서가 없어요.
              </div>
            )}
          </div>

          <div className="flex flex-col gap-3">
            <FormListItem
              selected={
                !!(
                  adoptionDetail?.agreements.guidelines &&
                  adoptionDetail?.agreements.monitoring
                )
              }
              disabled
              className="pointer-events-none justify-start text-left"
            >
              {adoptionDetail?.agreements.guidelines &&
              adoptionDetail?.agreements.monitoring
                ? "모든 동의 사항에 동의했어요."
                : "아직 모든 동의가 완료되지 않았어요."}
            </FormListItem>
          </div>
        </div>
      </Container>
    </div>
  );
}
