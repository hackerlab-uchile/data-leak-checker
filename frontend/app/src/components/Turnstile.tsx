import { useAuth } from "@/contexts/AuthContext";
import { Button } from "./ui/button";
import Link from "next/link";
import { useRouter } from "next/router";
import { RiArrowDropDownLine } from "react-icons/ri";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { FaCircleUser } from "react-icons/fa6";
import { useEffect, useRef, useState } from "react";
import { Separator } from "./ui/separator";
import { IoLogOutOutline } from "react-icons/io5";
import Script from "next/script";

export default function Turnstile({
  siteKey,
  onTokenChange,
  onErrorCallback,
}: {
  siteKey: string;
  onTokenChange?: (token: string | null) => void;
  onErrorCallback?: () => void;
}) {
  const turnstileRef = useRef<HTMLDivElement | null>(null);
  const [turnstileLoaded, setTurnstileLoaded] = useState(false);

  useEffect(() => {
    const checkTurnstileLoaded = () => {
      onTokenChange?.(null);
      if (typeof (window as any).turnstile !== "undefined") {
        setTurnstileLoaded(true);
      } else {
        setTimeout(checkTurnstileLoaded, 100);
      }
    };

    checkTurnstileLoaded();
  }, []);

  useEffect(() => {
    if (turnstileLoaded && turnstileRef.current) {
      const widgetId = (window as any).turnstile.render(turnstileRef.current, {
        sitekey: siteKey, // Replace with your Turnstile site key
        callback: (token: string) => onTokenChange?.(token),
        "error-callback": () => {
          console.error("Turnstile challenge failed");
          onErrorCallback?.();
        },
        "expired-callback": () => {
          onTokenChange?.(null);
        },
      });
      return () => (window as any).turnstile.remove(widgetId);
    }
  }, [turnstileLoaded]);

  return (
    <>
      <Script
        src="https://challenges.cloudflare.com/turnstile/v0/api.js"
        async
        defer
      ></Script>
      <div ref={turnstileRef}></div>
    </>
  );
}
