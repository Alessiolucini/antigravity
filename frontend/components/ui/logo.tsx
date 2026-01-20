import Link from "next/link";
import { cn } from "@/lib/utils";

interface LogoProps {
    className?: string;
    variant?: "default" | "white" | "symbol";
    size?: "sm" | "md" | "lg";
}

export function Logo({ className, variant = "default", size = "md" }: LogoProps) {
    const heightClasses = {
        sm: "h-8",
        md: "h-12",
        lg: "h-16"
    };

    return (
        <Link href="/" className={cn("flex items-center transition-opacity hover:opacity-90", className)}>
            <img
                src="/logo.png"
                alt="Pronto Casa Logo"
                className={cn(
                    "w-auto object-contain",
                    heightClasses[size],
                    variant === "white" && "brightness-0 invert" // Simple way to make it white if needed
                )}
            />
        </Link>
    );
}
