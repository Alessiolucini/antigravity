"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";

export default function LoginPage() {
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        // TODO: Integrate with backend
        setTimeout(() => setIsLoading(false), 2000);
    };

    return (
        <div className="space-y-6">
            <div className="text-center space-y-2">
                <h1 className="text-2xl font-bold text-secondary">Bentornato</h1>
                <p className="text-neutral-500 text-sm">Inserisci le tue credenziali per accedere</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                    <Label htmlFor="email">Email o Telefono</Label>
                    <Input id="email" type="text" placeholder="mario.rossi@email.it" required />
                </div>
                <div className="space-y-2">
                    <div className="flex justify-between items-center">
                        <Label htmlFor="password">Password</Label>
                        <Link href="/auth/forgot-password" class="text-xs text-primary hover:underline">
                            Recupera
                        </Link>
                    </div>
                    <Input id="password" type="password" required />
                </div>

                <Button type="submit" className="w-full" isLoading={isLoading}>
                    Accedi
                </Button>
            </form>

            <div className="relative">
                <div className="absolute inset-0 flex items-center">
                    <span className="w-full border-t border-neutral-200" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                    <span className="bg-white px-2 text-neutral-400">Oppure</span>
                </div>
            </div>

            <div className="text-center text-sm text-neutral-600">
                Non hai un account?{" "}
                <Link href="/auth/register" className="font-bold text-primary hover:underline">
                    Registrati
                </Link>
            </div>
        </div>
    );
}
