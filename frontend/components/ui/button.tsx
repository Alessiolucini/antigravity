import { ButtonHTMLAttributes, forwardRef } from "react";
import { cn } from "@/lib/utils";
import { Loader2 } from "lucide-react";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: "primary" | "secondary" | "outline" | "ghost";
    size?: "sm" | "md" | "lg" | "icon";
    isLoading?: boolean;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant = "primary", size = "md", isLoading, children, ...props }, ref) => {
        const variants = {
            primary: "bg-primary text-white hover:bg-orange-600 shadow-md hover:shadow-lg",
            secondary: "bg-secondary text-white hover:bg-sky-800 shadow-md hover:shadow-lg",
            outline: "border-2 border-primary text-primary hover:bg-primary/10",
            ghost: "text-neutral-500 hover:text-primary hover:bg-neutral-100",
        };

        const sizes = {
            sm: "h-9 px-4 text-sm",
            md: "h-12 px-6 text-base",
            lg: "h-14 px-8 text-lg",
            icon: "h-10 w-10 p-0",
        };

        return (
            <button
                ref={ref}
                className={cn(
                    "inline-flex items-center justify-center rounded-xl font-bold transition-all duration-200 active:scale-95 disabled:pointer-events-none disabled:opacity-50",
                    variants[variant],
                    sizes[size],
                    className
                )}
                disabled={isLoading || props.disabled}
                {...props}
            >
                {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                {children}
            </button>
        );
    }
);
Button.displayName = "Button";

export { Button };
