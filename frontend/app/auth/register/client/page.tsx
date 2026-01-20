"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function ClientRegisterPage() {
    return (
        <div className="space-y-6">
            <div className="text-center space-y-2">
                <h1 className="text-2xl font-bold text-secondary">Registrazione Cliente</h1>
                <p className="text-neutral-500 text-sm">Inserisci i tuoi dati per iniziare</p>
            </div>

            <form className="space-y-4">
                <div className="space-y-2">
                    <Label htmlFor="name">Nome e Cognome</Label>
                    <Input id="name" type="text" placeholder="Mario Rossi" required />
                </div>
                <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" type="email" placeholder="mario@esempio.it" required />
                </div>
                <div className="space-y-2">
                    <Label htmlFor="password">Password</Label>
                    <Input id="password" type="password" required />
                </div>

                <Button type="submit" className="w-full">Crea Account</Button>
            </form>
        </div>
    );
}
