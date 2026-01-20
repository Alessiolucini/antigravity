import Link from "next/link";
import { cn } from "@/lib/utils";

interface LogoProps {
    className?: string;
    variant?: "default" | "white" | "symbol";
    size?: "sm" | "md" | "lg";
}

export function Logo({ className, variant = "default", size = "md" }: LogoProps) {
    const sizeClasses = {
        sm: "h-8 w-8",
        md: "h-10 w-10",
        lg: "h-12 w-12"
    };

    const iconSizes = {
        sm: "h-5 w-5",
        md: "h-6 w-6",
        lg: "h-7 w-7"
    };

    const textSizes = {
        sm: "text-lg",
        md: "text-xl",
        lg: "text-2xl"
    };
    return (
        <Link href="/" className={cn("flex items-center gap-2 transition-opacity hover:opacity-90", className)}>
            <div className={cn(
                "flex items-center justify-center rounded-lg shadow-sm border",
                sizeClasses[size],
                variant === "white" ? "bg-white text-primary border-white" : "bg-primary text-white border-primary"
            )}>
                {/* House Icon with Wrench - Simplified SVG */}
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className={iconSizes[size]}>
                    <path d="M3 10l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                    <path d="M14.5 11.5l2 2" />
                    <path d="M12 14l2-2" />
                </svg>
            </div>

            {variant !== "symbol" && (
                <div className="flex flex-col">
                    <span className={cn(
                        "font-black leading-none tracking-tight",
                        textSizes[size],
                        variant === "white" ? "text-white" : "text-secondary"
                    )}>
                        PRONTO
                        <span className={cn(variant === "white" ? "text-white" : "text-primary")}>CASA</span>
                    </span>
                    <span className={cn(
                        "text-[0.6rem] font-medium tracking-wider uppercase",
                        variant === "white" ? "text-white/80" : "text-neutral-500"
                    )}>
                        Riparazioni Urgenti
                    </span>
                </div>
            )}
        </Link>
    );
}
