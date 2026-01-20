"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { AlertCircle, CheckCircle2 } from "lucide-react";

export default function TechnicianRegisterPage() {
    const [formData, setFormData] = useState({ name: "", email: "", password: "", specialization: "" });
    const [status, setStatus] = useState<{ type: "success" | "error"; message: string } | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setStatus(null);

        try {
            const response = await fetch("https://api.prontocasa.net/api/v1/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    ...formData,
                    role: "technician" // Assuming the backend supports role or handles it via data
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Errore durante la registrazione");
            }

            setStatus({ type: "success", message: "Candidatura inviata! Verrai ricontattato a breve." });
            setTimeout(() => {
                window.location.href = "/auth/login";
            }, 2000);
        } catch (error: any) {
            setStatus({ type: "error", message: error.message });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="space-y-6">
            <div className="text-center space-y-2">
                <h1 className="text-2xl font-bold text-secondary">Registrazione Tecnico</h1>
                <p className="text-neutral-500 text-sm">Unisciti alla nostra rete di professionisti</p>
            </div>

            {status && (
                <div className={`p-4 rounded-lg flex items-center gap-3 text-sm ${status.type === "success" ? "bg-green-50 text-green-700 border border-green-200" : "bg-red-50 text-red-700 border border-red-200"
                    }`}>
                    {status.type === "success" ? <CheckCircle2 className="w-5 h-5" /> : <AlertCircle className="w-5 h-5" />}
                    {status.message}
                </div>
            )}

            <form className="space-y-4" onSubmit={handleSubmit}>
                <div className="space-y-2">
                    <Label htmlFor="name">Nome e Cognome</Label>
                    <Input
                        id="name"
                        type="text"
                        placeholder="Mario Rossi"
                        required
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    />
                </div>
                <div className="space-y-2">
                    <Label htmlFor="specialization">Specializzazione</Label>
                    <Input
                        id="specialization"
                        type="text"
                        placeholder="Es. Idraulico, Elettricista..."
                        required
                        value={formData.specialization}
                        onChange={(e) => setFormData({ ...formData, specialization: e.target.value })}
                    />
                </div>
                <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                        id="email"
                        type="email"
                        placeholder="mario@esempio.it"
                        required
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    />
                </div>
                <div className="space-y-2">
                    <Label htmlFor="password">Password</Label>
                    <Input
                        id="password"
                        type="password"
                        required
                        value={formData.password}
                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    />
                </div>

                <Button type="submit" className="w-full bg-secondary hover:bg-sky-800" disabled={isLoading}>
                    {isLoading ? "Invio in corso..." : "Candidati Ora"}
                </Button>
            </form>
        </div>
    );
}
