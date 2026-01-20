"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ChevronRight, Euro, Clock } from "lucide-react";
import { motion } from "framer-motion";

export default function TechniciansPage() {
    const benefits = [
        {
            icon: <Euro className="h-10 w-10 text-secondary" />,
            title: "Guadagni Elevati",
            description: "Trattieni il 90% di ogni intervento. Pagamenti garantiti e trasparenti direttamente sul tuo conto."
        },
        {
            icon: <Clock className="h-10 w-10 text-secondary" />,
            title: "Flessibilità Totale",
            description: "Decidi tu quando essere online. Ricevi richieste solo nelle zone che preferisci coprire."
        }
    ];

    const steps = [
        { title: "Registrati", description: "Crea il tuo profilo professionale in pochi minuti." },
        { title: "Verifica", description: "Carica i tuoi documenti e certificazioni." },
        { title: "Lavora", description: "Ricevi notifiche in tempo reale e accetta interventi." },
        { title: "Guadagna", description: "Ricevi il pagamento appena l'intervento è concluso." }
    ];

    return (
        <div className="flex flex-col min-h-screen">
            {/* Hero Section */}
            <section className="relative pt-32 pb-20 overflow-hidden bg-neutral-900 text-white">
                <div className="container mx-auto px-4 relative z-10">
                    <div className="max-w-3xl">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5 }}
                        >
                            <span className="inline-block px-4 py-1 rounded-full bg-secondary/20 text-secondary text-sm font-bold mb-6 border border-secondary/30">
                                OPPORTUNITÀ PER PROFESSIONISTI
                            </span>
                            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
                                Fai crescere la tua attività con <span className="text-secondary">Pronto Casa</span>
                            </h1>
                            <p className="text-xl text-neutral-400 mb-10 leading-relaxed">
                                Unisciti alla rete n.1 in Italia per le riparazioni domestiche. Ricevi clienti qualificati, gestisci tutto da app e dimentica la burocrazia.
                            </p>
                            <div className="flex flex-col sm:flex-row gap-4">
                                <Link href="/auth/register/technician">
                                    <Button size="lg" className="bg-secondary hover:bg-sky-800 text-white px-8 h-14 text-lg w-full sm:w-auto">
                                        Inizia Ora
                                        <ChevronRight className="ml-2 h-5 w-5" />
                                    </Button>
                                </Link>
                                <Link href="/auth/login">
                                    <Button size="lg" variant="outline" className="border-white/20 text-white hover:bg-white/10 px-8 h-14 text-lg w-full sm:w-auto">
                                        Accedi al Portale
                                    </Button>
                                </Link>
                            </div>
                        </motion.div>
                    </div>
                </div>

                {/* Background Decoration */}
                <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-secondary/10 to-transparent hidden lg:block" />
            </section>

            {/* Benefits Grid */}
            <section className="py-24 bg-white">
                <div className="container mx-auto px-4">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl font-bold mb-4 text-neutral-900">Perché scegliere noi?</h2>
                        <p className="text-neutral-500 max-w-2xl mx-auto">Abbiamo reinventato il modo in cui i professionisti trovano lavoro, mettendo al centro la qualità e la trasparenza.</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                        {benefits.map((benefit, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: index * 0.1 }}
                                className="p-8 rounded-2xl border border-neutral-100 hover:border-secondary/20 hover:shadow-xl hover:shadow-secondary/5 transition-all duration-300 group"
                            >
                                <div className="mb-6 p-3 rounded-xl bg-neutral-50 group-hover:bg-secondary/10 transition-colors w-fit">
                                    {benefit.icon}
                                </div>
                                <h3 className="text-xl font-bold mb-3 text-neutral-900">{benefit.title}</h3>
                                <p className="text-neutral-500 leading-relaxed">{benefit.description}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* How it Works */}
            <section className="py-24 bg-neutral-50">
                <div className="container mx-auto px-4">
                    <div className="bg-neutral-900 rounded-[3rem] p-8 md:p-16 relative overflow-hidden text-white">
                        <div className="relative z-10">
                            <h2 className="text-4xl font-bold mb-16 text-center">Inizia in 4 passaggi</h2>
                            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative">
                                {steps.map((step, index) => (
                                    <div key={index} className="relative text-center md:text-left">
                                        <div className="text-6xl font-black text-white/10 mb-4">{index + 1}</div>
                                        <h3 className="text-xl font-bold mb-3">{step.title}</h3>
                                        <p className="text-neutral-400 text-sm leading-relaxed">{step.description}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-24 bg-white text-center">
                <div className="container mx-auto px-4 border-y border-neutral-100 py-20">
                    <h2 className="text-4xl font-bold mb-6 text-neutral-900">Sei pronto a rivoluzionare il tuo lavoro?</h2>
                    <p className="text-xl text-neutral-500 mb-10 max-w-2xl mx-auto">
                        Migliaia di interventi vengono richiesti ogni mese. Non perdere l&apos;opportunità di far parte dell&apos;élite dei tecnici italiani.
                    </p>
                    <Link href="/auth/register/technician">
                        <Button size="lg" className="bg-secondary hover:bg-sky-800 text-white px-12 h-16 text-xl rounded-full shadow-lg shadow-secondary/20">
                            Inviaci la tua candidatura
                        </Button>
                    </Link>
                </div>
            </section>
        </div>
    );
}
