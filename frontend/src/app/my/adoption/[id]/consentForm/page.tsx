"use client";

import React, { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { ArrowLeft } from "@phosphor-icons/react";
import { useGetUserAdoptionDetail } from "@/hooks/query/useGetUserAdoptionDetail";
import { useGetCenterConsents } from "@/hooks/query/useGetCenterConsents";

import { Container } from "@/components/common/Container";
import { TopBar } from "@/components/common/TopBar";
import { IconButton } from "@/components/ui/IconButton";
import { FormListItem } from "@/components/ui/FormListItem";

interface ConsentFormPageProps {
  params: Promise<{ id: string }>;
}

export default function ConsentFormPage({ params }: ConsentFormPageProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { id } = React.use(params);

  const [guidelinesContent, setGuidelinesContent] = useState<string>("");

  const handleBack = () => {
    router.back();
  };

  const {
    data: adoptionDetail,
    isLoading,
    error,
  } = useGetUserAdoptionDetail({
    adoptionId: id,
  });

  // 센터의 동의서 목록 조회
  const {
    data: centerConsents,
    isLoading: isConsentsLoading,
    error: consentsError,
  } = useGetCenterConsents(adoptionDetail?.adoption?.center_id || "");

  const activeConsents = React.useMemo(
    () => centerConsents?.filter((consent) => consent.is_active) ?? [],
    [centerConsents]
  );
  const fallbackConsent = React.useMemo(
    () => activeConsents[0] ?? centerConsents?.[0] ?? null,
    [activeConsents, centerConsents]
  );

  useEffect(() => {
    // URL 쿼리 파라미터에서 guidelines 내용 가져오기
    const guidelines = searchParams.get("guidelines");
    if (guidelines) {
      setGuidelinesContent(decodeURIComponent(guidelines));
    } else if (adoptionDetail?.contract?.guidelines_content) {
      // API에서 가져온 guidelines 내용 사용
      setGuidelinesContent(adoptionDetail.contract.guidelines_content);
    }
  }, [searchParams, adoptionDetail]);

  useEffect(() => {
    if (!guidelinesContent && fallbackConsent?.content) {
      setGuidelinesContent(fallbackConsent.content);
    }
  }, [fallbackConsent, guidelinesContent]);

  // 페이지 접근 시 스크롤 최상단으로 이동
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [id]);

  if (isLoading || isConsentsLoading) {
    return (
      <Container className="min-h-screen">
        <TopBar
          variant="variant4"
          left={
            <div className="flex items-center gap-2">
              <IconButton
                icon={({ size }) => <ArrowLeft size={size} weight="bold" />}
                size="iconM"
                onClick={() => router.back()}
              />
              <h4>동의서</h4>
            </div>
          }
        />
        <div className="flex flex-col gap-3 px-4 py-4">
          <div className="text-center py-8">로딩 중...</div>
        </div>
      </Container>
    );
  }

  if (error || consentsError || !adoptionDetail) {
    return (
      <Container className="min-h-screen">
        <TopBar
          variant="variant4"
          left={
            <div className="flex items-center gap-2">
              <IconButton
                icon={({ size }) => <ArrowLeft size={size} weight="bold" />}
                size="iconM"
                onClick={() => router.back()}
              />
              <h4>동의서</h4>
            </div>
          }
        />
        <div className="flex flex-col gap-3 px-4 py-4">
          <div className="text-center py-8 text-red-500">
            오류가 발생했습니다.
          </div>
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
                {fallbackConsent?.title ?? "동의서 내용"}
              </h2>
              <p className="body2 text-gr">
                {fallbackConsent?.description ??
                  "입양 절차와 관련된 동의서 내용을 확인해주세요."}
              </p>
            </div>
            {guidelinesContent || fallbackConsent?.content ? (
              <div className="flex flex-col gap-6">
                <div className="body text-dg whitespace-pre-wrap leading-relaxed">
                  {guidelinesContent || fallbackConsent?.content}
                </div>
              </div>
            ) : (
              <div className="rounded-lg border border-lg bg-white px-4 py-6 text-center text-gr">
                동의서 내용이 준비되지 않았습니다.
              </div>
            )}
          </div>
          <div className="flex flex-col gap-3">
            <div className="flex flex-col gap-2">
              <FormListItem
                selected={
                  !!(
                    adoptionDetail?.adoption.guidelines_agreement &&
                    adoptionDetail?.adoption.monitoring_agreement
                  )
                }
                disabled
                className="pointer-events-none justify-start text-left"
              >
                모든 동의 사항에 동의했어요.
              </FormListItem>
            </div>
          </div>
        </div>
      </Container>
    </div>
  );
}
