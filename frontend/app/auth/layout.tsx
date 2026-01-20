import { Logo } from "@/components/ui/logo";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function AuthLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen bg-neutral-50 flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-md space-y-8">
                <div className="flex flex-col items-center text-center">
                    <Link href="/" className="mb-8 hover:opacity-80 transition-opacity">
                        <Logo size="lg" />
                    </Link>
                </div>

                <div className="bg-white p-8 rounded-3xl shadow-xl border border-neutral-100">
                    {children}
                </div>

                <div className="text-center">
                    <Link href="/" className="inline-flex items-center text-sm text-neutral-500 hover:text-primary transition-colors">
                        <ArrowLeft className="w-4 h-4 mr-1" />
                        Torna alla Home
                    </Link>
                </div>
            </div>
        </div>
    );
}
