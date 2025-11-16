import React from "react";

export default function Layout({
  children,
  overlay,
}: {
  children: React.ReactNode;
  overlay: React.ReactNode;
}) {
  return (
    <>
      {children}
      {overlay}
    </>
  );
}
