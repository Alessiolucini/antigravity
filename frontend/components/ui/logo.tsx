import Link from "next/link";
import { cn } from "@/lib/utils";

interface LogoProps {
    className?: string;
    variant?: "default" | "white" | "symbol";
    size?: "sm" | "md" | "lg";
}

export function Logo({ className, variant = "default", size = "md" }: LogoProps) {
    const heightClasses = {
        sm: "h-10",
        md: "h-16",
        lg: "h-24"
    };

    return (
        <Link href="/" className={cn("flex items-center transition-opacity hover:opacity-90 leading-none", className)}>
            <img
                src="/logo.png"
                alt="Pronto Casa Logo"
                className={cn(
                    "w-auto h-full object-contain mix-blend-multiply",
                    heightClasses[size],
                    variant === "white" && "brightness-0 invert mix-blend-screen" // mix-blend-screen works better for white on dark
                )}
            />
        </Link>
    );
}
