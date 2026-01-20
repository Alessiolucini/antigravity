"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { Wrench, Zap, Key, Droplet, Hammer, Thermometer, Clock, ShieldCheck, Star } from "lucide-react";
import { motion } from "framer-motion";

export default function Home() {
  const services = [
    { icon: Droplet, name: "Idraulico", desc: "Perdite, tubi rotti, sanitari" },
    { icon: Zap, name: "Elettricisita", desc: "Cortocircuiti, prese, impianti" },
    { icon: Key, name: "Fabbro", desc: "Serrature bloccate, porte" },
    { icon: Thermometer, name: "Caldaie & Clima", desc: "Riparazioni e manutenzione" },
    { icon: Hammer, name: "Tuttofare", desc: "Montaggio mobili, riparazioni" },
    { icon: Wrench, name: "Elettrodomestici", desc: "Lavartici, frigo, forni" },
  ];

  const steps = [
    {
      title: "1. Descrivi il problema",
      desc: "Rispondi a poche domande e carica una foto o video del guasto.",
      icon: "📱"
    },
    {
      title: "2. Ricevi il preventivo",
      desc: "L'IA analizza il danno e ti dà una stima immediata dei costi.",
      icon: "🤖"
    },
    {
      title: "3. Il tecnico arriva",
      desc: "Segui l'arrivo del professionista in tempo reale sulla mappa.",
      icon: "📍"
    },
  ];

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  return (
    <div className="min-h-screen flex flex-col font-sans">
      <Navbar />

      <main className="flex-grow">
        {/* HERO SECTION */}
        <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
          {/* Background Gradient */}
          <div className="absolute inset-0 bg-gradient-to-br from-slate-50 to-orange-50 -z-20" />
          <div className="absolute top-0 right-0 w-1/2 h-full bg-orange-100/30 -skew-x-12 -z-10 blur-3xl rounded-full translate-x-1/4" />

          <div className="container mx-auto px-4 grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-6"
            >
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-orange-100 text-primary text-sm font-bold uppercase tracking-wider">
                <Clock className="w-4 h-4" />
                Interventi in <span className="underline decoration-2 underline-offset-2">30 minuti</span>
              </div>

              <h1 className="text-5xl lg:text-7xl font-extrabold text-secondary leading-[1.1]">
                Riparazioni Urgenti<br />
                <span className="text-primary">a Portata di App</span>
              </h1>

              <p className="text-xl text-neutral-600 max-w-lg leading-relaxed">
                Il modo più veloce e sicuro per trovare idraulici, elettricisti e fabbri professionisti.
                Prezzi chiari, zero sorprese.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <Link href="/request">
                  <Button size="lg" className="w-full sm:w-auto text-lg px-8 shadow-xl shadow-orange-500/20">
                    Richiedi Intervento
                  </Button>
                </Link>
                <Link href="#how-it-works">
                  <Button variant="outline" size="lg" className="w-full sm:w-auto text-lg">
                    Come Funziona
                  </Button>
                </Link>
              </div>

              <div className="flex items-center gap-4 text-sm font-medium text-neutral-500 pt-4">
                <div className="flex items-center gap-1">
                  <ShieldCheck className="w-5 h-5 text-green-500" />
                  Professionisti Verificati
                </div>
                <div className="flex items-center gap-1">
                  <Star className="w-5 h-5 text-yellow-400 fill-current" />
                  4.9/5 Recensioni
                </div>
              </div>
            </motion.div>

            {/* Hero Image / Illustration Placeholder */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="relative"
            >
              <div className="aspect-square rounded-[3rem] bg-gradient-to-tr from-secondary to-blue-900 shadow-2xl relative overflow-hidden group">
                <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=2069&auto=format&fit=crop')] bg-cover bg-center opacity-80 mix-blend-overlay transition-opacity duration-700 group-hover:opacity-90"></div>
                <div className="absolute inset-0 bg-gradient-to-t from-secondary/80 to-transparent"></div>

                {/* Floating Card 1 */}
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.6 }}
                  className="absolute bottom-8 left-8 bg-white p-4 rounded-2xl shadow-lg max-w-[200px]"
                >
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                      <ShieldCheck className="w-6 h-6 text-green-600" />
                    </div>
                    <div>
                      <p className="font-bold text-secondary text-sm">Garantito</p>
                      <p className="text-xs text-neutral-500">Assicurazione inclusa</p>
                    </div>
                  </div>
                </motion.div>

                {/* Floating Card 2 */}
                <motion.div
                  initial={{ x: 20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.8 }}
                  className="absolute top-12 right-8 bg-white/90 backdrop-blur p-4 rounded-2xl shadow-lg"
                >
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
                    <span className="font-bold text-secondary text-sm">Tecnici Disponibili: 24</span>
                  </div>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* SERVICES GRID */}
        <section id="services" className="py-24 bg-white">
          <div className="container mx-auto px-4">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <h2 className="text-4xl font-bold text-secondary mb-4">Di cosa hai bisogno?</h2>
              <p className="text-neutral-600 text-lg">
                Seleziona la categoria del problema. I nostri tecnici specializzati sono pronti a intervenire per ogni emergenza domestica.
              </p>
            </div>

            <motion.div
              variants={container}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true }}
              className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6"
            >
              {services.map((service, index) => (
                <motion.div key={index} variants={item}>
                  <Link href={`/request?category=${service.name.toLowerCase()}`} className="block group h-full">
                    <div className="h-full p-6 rounded-2xl bg-neutral-50 border border-neutral-100 hover:border-primary/30 hover:shadow-lg hover:shadow-orange-500/5 transition-all duration-300 flex flex-col items-center text-center gap-4 group-hover:-translate-y-1">
                      <div className="w-16 h-16 rounded-2xl bg-white shadow-sm flex items-center justify-center group-hover:bg-primary group-hover:text-white transition-colors duration-300">
                        <service.icon className="w-8 h-8 text-primary group-hover:text-white transition-colors" />
                      </div>
                      <div>
                        <h3 className="font-bold text-secondary mb-1">{service.name}</h3>
                        <p className="text-xs text-neutral-500 leading-tight">{service.desc}</p>
                      </div>
                    </div>
                  </Link>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>

        {/* HOW IT WORKS */}
        <section id="how-it-works" className="py-24 bg-neutral-50 relative overflow-hidden">
          <div className="container mx-auto px-4">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-secondary mb-4">Come funziona Pronto Casa</h2>
              <p className="text-neutral-600">Risolvere un problema non è mai stato così semplice.</p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 relative">
              {/* Connector Line (Desktop) */}
              <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-0.5 bg-neutral-200 -z-10" />

              {steps.map((step, index) => (
                <div key={index} className="relative flex flex-col items-center text-center">
                  <div className="w-24 h-24 rounded-3xl bg-white shadow-md flex items-center justify-center text-4xl mb-6 z-10 border-4 border-neutral-50">
                    {step.icon}
                  </div>
                  <h3 className="text-xl font-bold text-secondary mb-3">{step.title}</h3>
                  <p className="text-neutral-600 max-w-xs">{step.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA TECHNICIAN */}
        <section className="py-24 bg-secondary text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 w-96 h-96 bg-primary/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />

          <div className="container mx-auto px-4 relative z-10">
            <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 md:p-12 border border-white/20 flex flex-col md:flex-row items-center justify-between gap-8">
              <div className="max-w-xl">
                <h2 className="text-3xl md:text-4xl font-bold mb-4">Sei un professionista?</h2>
                <p className="text-blue-100 text-lg mb-0">
                  Unisciti alla rete di Pronto Casa. Ricevi richieste verificate nella tua zona, gestisci i tuoi orari e fatti pagare puntualmente. Zero costi fissi.
                </p>
              </div>
              <div className="shrink-0">
                <Link href="/auth/register?role=technician">
                  <Button size="lg" className="bg-white text-secondary hover:bg-neutral-100 text-lg px-8 border-none">
                    Diventa un Partner
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
