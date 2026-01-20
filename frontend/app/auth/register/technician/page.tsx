"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function TechnicianRegisterPage() {
    return (
        <div className="space-y-6">
            <div className="text-center space-y-2">
                <h1 className="text-2xl font-bold text-secondary">Registrazione Tecnico</h1>
                <p className="text-neutral-500 text-sm">Unisciti alla nostra rete di professionisti</p>
            </div>

            <form className="space-y-4">
                <div className="space-y-2">
                    <Label htmlFor="name">Nome e Cognome</Label>
                    <Input id="name" type="text" placeholder="Mario Rossi" required />
                </div>
                <div className="space-y-2">
                    <Label htmlFor="specialization">Specializzazione</Label>
                    <Input id="specialization" type="text" placeholder="Es. Idraulico, Elettricista..." required />
                </div>
                <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" type="email" placeholder="mario@esempio.it" required />
                </div>
                <div className="space-y-2">
                    <Label htmlFor="password">Password</Label>
                    <Input id="password" type="password" required />
                </div>

                <Button type="submit" className="w-full bg-secondary hover:bg-sky-800">Candidati Ora</Button>
            </form>
        </div>
    );
}
