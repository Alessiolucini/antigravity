"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
    Droplet, Zap, Key, Thermometer, Hammer, Wrench,
    ArrowLeft, ArrowRight, Camera, Upload, AlertCircle,
    CheckCircle2, Clock, ShieldCheck
} from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";

const services = [
    { id: "idraulico", icon: Droplet, name: "Idraulico", desc: "Perdite, tubi rotti, sanitari" },
    { id: "elettricisita", icon: Zap, name: "Elettricisita", desc: "Cortocircuiti, prese, impianti" },
    { id: "fabbro", icon: Key, name: "Fabbro", desc: "Serrature bloccate, porte" },
    { id: "caldaie", icon: Thermometer, name: "Caldaie & Clima", desc: "Riparazioni e manutenzione" },
    { id: "tuttofare", icon: Hammer, name: "Tuttofare", desc: "Montaggio mobili, riparazioni" },
    { id: "elettrodomestici", icon: Wrench, name: "Elettrodomestici", desc: "Lavartici, frigo, forni" },
];

function RequestPageBody() {
    const searchParams = useSearchParams();
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        category: searchParams.get("category") || "",
        description: "",
        urgency: "Normal",
        address: "",
        contact: ""
    });

    useEffect(() => {
        const cat = searchParams.get("category");
        if (cat) {
            setFormData(prev => ({ ...prev, category: cat }));
            setStep(2);
        }
    }, [searchParams]);

    const nextStep = () => setStep(prev => prev + 1);
    const prevStep = () => setStep(prev => prev - 1);

    return (
        <main className="flex-grow pt-24 pb-12">
            <div className="container mx-auto px-4 max-w-2xl">
                {/* Progress Bar */}
                <div className="mb-12">
                    <div className="flex justify-between mb-2">
                        {[1, 2, 3, 4].map((s) => (
                            <div
                                key={s}
                                className={`w-1/4 h-2 rounded-full mx-1 transition-all duration-500 ${step >= s ? "bg-primary" : "bg-neutral-200"
                                    }`}
                            />
                        ))}
                    </div>
                    <div className="text-center text-xs font-bold text-neutral-400 uppercase tracking-widest">
                        Passaggio {step} di 4
                    </div>
                </div>

                <AnimatePresence mode="wait">
                    {step === 1 && (
                        <motion.div
                            key="step1"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            className="space-y-8"
                        >
                            <div className="text-center space-y-2">
                                <h1 className="text-3xl font-bold text-secondary">Di cosa hai bisogno?</h1>
                                <p className="text-neutral-500">Seleziona la categoria del tuo problema per iniziare.</p>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                {services.map((service) => (
                                    <button
                                        key={service.id}
                                        onClick={() => {
                                            setFormData({ ...formData, category: service.id });
                                            nextStep();
                                        }}
                                        className={`p-6 rounded-2xl border-2 text-left transition-all duration-200 group ${formData.category === service.id
                                                ? "border-primary bg-orange-50"
                                                : "border-white bg-white hover:border-orange-100"
                                            }`}
                                    >
                                        <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 transition-colors ${formData.category === service.id ? "bg-primary text-white" : "bg-neutral-100 text-primary group-hover:bg-primary group-hover:text-white"
                                            }`}>
                                            <service.icon className="w-6 h-6" />
                                        </div>
                                        <h3 className="font-bold text-secondary">{service.name}</h3>
                                        <p className="text-xs text-neutral-500 leading-tight">{service.desc}</p>
                                    </button>
                                ))}
                            </div>
                        </motion.div>
                    )}

                    {step === 2 && (
                        <motion.div
                            key="step2"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            className="space-y-8"
                        >
                            <div className="flex items-center gap-4">
                                <Button variant="ghost" size="icon" onClick={prevStep} className="rounded-full outline-none border-none">
                                    <ArrowLeft className="w-5 h-5" />
                                </Button>
                                <div className="space-y-1">
                                    <h1 className="text-2xl font-bold text-secondary text-left">Descrivi il problema</h1>
                                    <p className="text-neutral-500 text-sm">Più dettagli fornisci, più preciso sarà il preventivo.</p>
                                </div>
                            </div>

                            <div className="bg-white p-8 rounded-3xl shadow-xl border border-neutral-100 space-y-6">
                                <div className="space-y-4">
                                    <Label htmlFor="description" className="text-lg">Cosa è successo?</Label>
                                    <textarea
                                        id="description"
                                        rows={4}
                                        className="w-full p-4 rounded-xl border border-neutral-200 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all resize-none"
                                        placeholder="Esempio: Il rubinetto in cucina perde acqua da ieri sera..."
                                        value={formData.description}
                                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                    />
                                </div>

                                <div className="space-y-4">
                                    <Label className="text-lg">Carica foto o video</Label>
                                    <div className="grid grid-cols-2 gap-4">
                                        <button className="flex flex-col items-center justify-center gap-2 p-8 border-2 border-dashed border-neutral-200 rounded-2xl hover:border-primary hover:bg-orange-50 transition-all text-neutral-400 hover:text-primary group">
                                            <Camera className="w-8 h-8" />
                                            <span className="text-xs font-bold uppercase tracking-wider">Scatta Foto</span>
                                        </button>
                                        <button className="flex flex-col items-center justify-center gap-2 p-8 border-2 border-dashed border-neutral-200 rounded-2xl hover:border-primary hover:bg-orange-50 transition-all text-neutral-400 hover:text-primary group">
                                            <Upload className="w-8 h-8" />
                                            <span className="text-xs font-bold uppercase tracking-wider">Libreria</span>
                                        </button>
                                    </div>
                                </div>

                                <Button
                                    onClick={nextStep}
                                    className="w-full"
                                    size="lg"
                                    disabled={!formData.description}
                                >
                                    Continua
                                    <ArrowRight className="w-5 h-5 ml-2" />
                                </Button>
                            </div>
                        </motion.div>
                    )}

                    {step === 3 && (
                        <motion.div
                            key="step3"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            className="space-y-8"
                        >
                            <div className="text-center space-y-4">
                                <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-blue-100 text-blue-600 mb-4 animate-pulse">
                                    <Clock className="w-10 h-10" />
                                </div>
                                <h1 className="text-3xl font-bold text-secondary">Analisi IA in corso...</h1>
                                <p className="text-neutral-500">Stiamo elaborando le informazioni per darti la migliore stima.</p>
                            </div>

                            <div className="bg-white p-8 rounded-3xl shadow-xl border-t-4 border-t-blue-500 space-y-6">
                                <div className="space-y-6">
                                    <div className="flex items-start gap-4 p-4 bg-blue-50 rounded-2xl border border-blue-100">
                                        <AlertCircle className="w-6 h-6 text-blue-600 shrink-0 mt-1" />
                                        <div>
                                            <h3 className="font-bold text-blue-900">Diagnosi Preliminare</h3>
                                            <p className="text-sm text-blue-800">In base alla descrizione, sembra trattarsi di un guasto alla guarnizione principale dello scarico.</p>
                                        </div>
                                    </div>

                                    <div className="space-y-4">
                                        <div className="flex justify-between items-end border-b border-neutral-100 pb-4">
                                            <span className="text-neutral-500">Intervento stimato</span>
                                            <span className="text-3xl font-bold text-secondary">€60 - €85</span>
                                        </div>
                                        <div className="flex justify-between items-center text-sm">
                                            <span className="text-neutral-500">Arrivo previsto entro</span>
                                            <span className="font-bold text-green-600 flex items-center gap-1">
                                                <Clock className="w-4 h-4" /> 25 min
                                            </span>
                                        </div>
                                    </div>

                                    <div className="p-4 rounded-xl bg-neutral-50 border border-neutral-100 space-y-2">
                                        <div className="flex items-center gap-2 text-xs font-bold text-neutral-400 uppercase tracking-widest">
                                            <ShieldCheck className="w-4 h-4" /> Garanzia Pronto Casa
                                        </div>
                                        <p className="text-xs text-neutral-500">
                                            Il prezzo finale sarà confermato dal tecnico sul posto. Se non accetti il preventivo dopo l'ispezione, pagherai solo €20 per l'uscita.
                                        </p>
                                    </div>
                                </div>

                                <div className="flex flex-col gap-3">
                                    <Button onClick={nextStep} className="w-full" size="lg">
                                        Conferma e Richiedi
                                        <ArrowRight className="w-5 h-5 ml-2" />
                                    </Button>
                                    <Button variant="ghost" onClick={prevStep} className="w-full text-neutral-400 border-none outline-none">
                                        Modifica Richiesta
                                    </Button>
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {step === 4 && (
                        <motion.div
                            key="step4"
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="text-center space-y-8 py-12"
                        >
                            <div className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-green-100 text-green-600 mb-6">
                                <CheckCircle2 className="w-16 h-16" />
                            </div>

                            <div className="space-y-4">
                                <h1 className="text-4xl font-extrabold text-secondary">Richiesta Inviata!</h1>
                                <p className="text-xl text-neutral-600 max-w-md mx-auto">
                                    Abbiamo ricevuto il tuo SOS. Stiamo assegnando il miglior tecnico nella tua zona.
                                </p>
                            </div>

                            <div className="bg-white p-8 rounded-3xl shadow-xl border border-neutral-100 space-y-6 max-w-sm mx-auto">
                                <div className="space-y-2">
                                    <p className="text-xs font-bold text-neutral-400 uppercase tracking-widest">Codice Richiesta</p>
                                    <p className="text-xl font-mono font-bold text-secondary">PC-48291</p>
                                </div>

                                <div className="space-y-4">
                                    <div className="flex items-center gap-4 text-left p-4 bg-neutral-50 rounded-2xl">
                                        <div className="w-12 h-12 rounded-full bg-neutral-200 animate-pulse overflow-hidden relative">
                                            {/* Technician photo placeholder */}
                                        </div>
                                        <div>
                                            <p className="text-sm font-bold text-secondary">Ricerca tecnico...</p>
                                            <p className="text-xs text-neutral-500">Ti invieremo un SMS tra pochi secondi.</p>
                                        </div>
                                    </div>
                                </div>

                                <Link href="/">
                                    <Button variant="outline" className="w-full">
                                        Torna alla Home
                                    </Button>
                                </Link>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </main>
    );
}

export default function RequestPage() {
    return (
        <div className="min-h-screen flex flex-col bg-neutral-50">
            <Navbar />
            <Suspense fallback={<div className="pt-32 text-center text-secondary font-bold">Caricamento in corso...</div>}>
                <RequestPageBody />
            </Suspense>
            <Footer />
        </div>
    );
}
